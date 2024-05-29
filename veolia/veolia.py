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
    mqtt_client = mqtt.Client(mqtt.Client.CallbackAPIVersion.VERSION1)
    if mqtt_username:
        mqtt_client.username_pw_set(mqtt_username, mqtt_password)
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)
    mqtt_client.publish(topic, payload, retain=retain)
    mqtt_client.disconnect()

def publish_discovery():
    unique_id_prefix = "veolia_test_"
    device_name = "Veolia Water Consumption"
    device = {
        "identifiers": [unique_id_prefix + "water_meter"],
        "name": device_name,
        "model": "Veolia Water Meter",
        "manufacturer": "Veolia"
    }

    discovery_data = [
        {
            "name": "Veolia Daily Consumption",
            "state_topic": "homeassistant/sensor/veolia/daily/state",
            "unit_of_measurement": "L",
            "value_template": "{{ value_json.history[0][1] }}",
            "unique_id": unique_id_prefix + "daily_consumption",
            "device": device
        },
        {
            "name": "Veolia Monthly Consumption",
            "state_topic": "homeassistant/sensor/veolia/monthly/state",
            "unit_of_measurement": "L",
            "value_template": "{{ value_json.history[0][1] }}",
            "unique_id": unique_id_prefix + "monthly_consumption",
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
    publish_to_mqtt("homeassistant/sensor/veolia/daily/state", data_daily_json)
except Exception as e:
    print(f"Erreur lors de la récupération des données journalières: {e}")

# Récupérer les données de consommation mensuelle
try:
    data_monthly = client.update(month=True)
    print("Données de consommation mensuelle :")
    data_monthly_json = json.dumps({"history": data_monthly}, default=str)
    print(data_monthly_json)
    publish_to_mqtt("homeassistant/sensor/veolia/monthly/state", data_monthly_json)
except Exception as e:
    print(f"Erreur lors de la récupération des données mensuelles: {e}")
