import json
import os
import requests
import paho.mqtt.client as mqtt
from veolia_client import VeoliaClient
from datetime import datetime, timezone

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
mqtt_broker = os.getenv("MQTT_BROKER")
mqtt_port = int(os.getenv("MQTT_PORT"))
mqtt_username = os.getenv("MQTT_USERNAME")
mqtt_password = os.getenv("MQTT_PASSWORD")
hass_host = os.getenv("HASS_HOST")
hass_token = os.getenv("HASS_TOKEN")

client = VeoliaClient(email=username, password=password)

def publish_to_mqtt(topic, payload, retain=False):
    mqtt_client = mqtt.Client()
    if mqtt_username:
        mqtt_client.username_pw_set(mqtt_username, mqtt_password)
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)
    mqtt_client.publish(topic, payload, retain=retain)
    mqtt_client.disconnect()
    print(f"Published to MQTT topic {topic}: {payload}")

def publish_discovery():
    device = {
        "identifiers": ["veolia_test"],
        "name": "Veolia Test",
        "model": "Veolia Water Meter",
        "manufacturer": "Veolia"
    }

    discovery_data = [
        {
            "name": "Daily Consumption Test",
            "state_topic": "homeassistant/sensor/veolia_daily_consumption_test/state",
            "unit_of_measurement": "L",
            "value_template": "{{ value }}",
            "unique_id": "veolia_daily_consumption_test",
            "device": device,
            "state_class": "total_increasing",
            "device_class": "water",
            "has_entity_name": True
        },
        {
            "name": "Monthly Consumption Test",
            "state_topic": "homeassistant/sensor/veolia_monthly_consumption_test/state",
            "unit_of_measurement": "L",
            "value_template": "{{ value }}",
            "unique_id": "veolia_monthly_consumption_test",
            "device": device,
            "state_class": "total_increasing",
            "device_class": "water",
            "has_entity_name": True
        }
    ]

    for sensor in discovery_data:
        topic = f"homeassistant/sensor/{sensor['unique_id']}/config"
        payload = json.dumps(sensor)
        publish_to_mqtt(topic, payload, retain=True)

def convert_data(data):
    return [(str(entry[0]), entry[1]) for entry in data]

def import_statistics(data):
    headers = {
        "Authorization": f"Bearer {hass_token}",
        "Content-Type": "application/json",
    }
    stats = []
    sum_state = 0
    for entry in data:
        timestamp, value = entry
        iso_timestamp = datetime.strptime(timestamp, "%Y-%m-%d").replace(hour=6, minute=0, second=0).replace(tzinfo=timezone.utc).isoformat(timespec='seconds')
        sum_state += value
        stat = {
            "start": iso_timestamp,
            "state": value,
            "sum": sum_state
        }
        stats.append(stat)

    payload = {
        "metadata": {
            "has_mean": False,
            "has_sum": True,
            "name": "Veolia Test Daily Consumption",
            "source": "veolia_test",
            "statistic_id": "sensor.veolia_test_daily_consumption_test",
            "unit_of_measurement": "L"
        },
        "stats": stats
    }

    url = f"{hass_host}/api/services/recorder/import_statistics"
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error importing statistics: {response.status_code} - {response.text}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
    else:
        print("Historical data imported successfully")

# Se connecter
try:
    client.login()
    print("Connexion réussie")
    publish_discovery()
except Exception as e:
    print(f"Erreur de connexion: {e}")

# Récupérer les données de consommation journalière et publier l'historique
try:
    data_daily = client.update(month=False)
    if data_daily:
        print("Données de consommation journalière récupérées avec succès")
        print(data_daily)
        data_daily_converted = convert_data(data_daily["history"])
        latest_daily_consumption = data_daily_converted[0][1]  # Dernière valeur de consommation journalière
        data_daily_json = json.dumps(latest_daily_consumption)
        print(f"Daily JSON: {data_daily_json}")
        publish_to_mqtt("homeassistant/sensor/veolia_daily_consumption_test/state", data_daily_json)
        # Import long-term statistics for the daily consumption sensor
        import_statistics(data_daily_converted)
    else:
        print("Aucune donnée de consommation journalière disponible")
except Exception as e:
    print(f"Erreur lors de la récupération des données journalières: {e}")

# Récupérer les données de consommation mensuelle sans publier l'historique
try:
    data_monthly = client.update(month=True)
    if data_monthly:
        print("Données de consommation mensuelle récupérées avec succès")
        print(data_monthly)
        latest_monthly_consumption = data_monthly["history"][0][1]  # Dernière valeur de consommation mensuelle
        data_monthly_json = json.dumps(latest_monthly_consumption)
        print(f"Monthly JSON: {data_monthly_json}")
        publish_to_mqtt("homeassistant/sensor/veolia_monthly_consumption_test/state", data_monthly_json)
    else:
        print("Aucune donnée de consommation mensuelle disponible")
except Exception as e:
    print(f"Erreur lors de la récupération des données mensuelles: {e}")
