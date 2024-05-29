import json
import os
import paho.mqtt.client as mqtt
from veolia_client import VeoliaClient

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
mqtt_broker = os.getenv("MQTT_BROKER")
mqtt_port = int(os.getenv("MQTT_PORT"))
mqtt_username = os.getenv("MQTT_USERNAME")
mqtt_password = os.getenv("MQTT_PASSWORD")

# Afficher les variables d'environnement pour le débogage
print(f"USERNAME: {username}")
print(f"PASSWORD: {password}")
print(f"MQTT_BROKER: {mqtt_broker}")
print(f"MQTT_PORT: {mqtt_port}")
print(f"MQTT_USERNAME: {mqtt_username}")
print(f"MQTT_PASSWORD: {mqtt_password}")

client = VeoliaClient(email=username, password=password)

def publish_to_mqtt(topic, payload, retain=False):
    mqtt_client = mqtt.Client()
    if mqtt_username:
        mqtt_client.username_pw_set(mqtt_username, mqtt_password)
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)
    mqtt_client.publish(topic, payload, retain=retain)
    mqtt_client.disconnect()

def publish_discovery():
    device_name = "Veolia Water Meter Test"
    device = {
        "identifiers": ["veolia_water_meter_test"],
        "name": device_name,
        "model": "Veolia Water Meter",
        "manufacturer": "Veolia"
    }

    discovery_data = [
        {
            "name": "Veolia Daily Consumption Test",
            "state_topic": "homeassistant/sensor/veolia_daily_consumption_test/state",
            "unit_of_measurement": "L",
            "value_template": "{{ value_json.history[0][1] }}",
            "unique_id": "veolia_daily_consumption_test",
            "device": device
        },
        {
            "name": "Veolia Monthly Consumption Test",
            "state_topic": "homeassistant/sensor/veolia_monthly_consumption_test/state",
            "unit_of_measurement": "L",
            "value_template": "{{ value_json.history[0][1] }}",
            "unique_id": "veolia_monthly_consumption_test",
            "device": device
        }
    ]

    for sensor in discovery_data:
        topic = f"homeassistant/sensor/{sensor['unique_id']}/config"
        payload = json.dumps(sensor)
        publish_to_mqtt(topic, payload, retain=True)

# Se connecter
try:
    client.login()
    print("Connexion réussie")
    publish_discovery()
except Exception as e:
    print(f"Erreur de connexion: {e}")

# Récupérer les données de consommation journalière
try:
    data_daily = client.update(month=False)
    print("Données de consommation journalière :")
    data_daily_json = json.dumps({"history": data_daily}, default=str)
    print(data_daily_json)
    publish_to_mqtt("homeassistant/sensor/veolia_daily_consumption_test/state", data_daily_json)
except Exception as e:
    print(f"Erreur lors de la récupération des données journalières: {e}")

# Récupérer les données de consommation mensuelle
try:
    data_monthly = client.update(month=True)
    print("Données de consommation mensuelle :")
    data_monthly_json = json.dumps({"history": data_monthly}, default=str)
    print(data_monthly_json)
    publish_to_mqtt("homeassistant/sensor/veolia_monthly_consumption_test/state", data_monthly_json)
except Exception as e:
    print(f"Erreur lors de la récupération des données mensuelles: {e}")
