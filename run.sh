#!/usr/bin/env bash
CONFIG_PATH=/data/options.json

USERNAME=$(jq --raw-output '.username' $CONFIG_PATH)
PASSWORD=$(jq --raw-output '.password' $CONFIG_PATH)
MQTT_BROKER=$(jq --raw-output '.mqtt_broker' $CONFIG_PATH)
MQTT_PORT=$(jq --raw-output '.mqtt_port' $CONFIG_PATH)
MQTT_USERNAME=$(jq --raw-output '.mqtt_username' $CONFIG_PATH)
MQTT_PASSWORD=$(jq --raw-output '.mqtt_password' $CONFIG_PATH)

export USERNAME
export PASSWORD
export MQTT_BROKER
export MQTT_PORT
export MQTT_USERNAME
export MQTT_PASSWORD

# Afficher les variables d'environnement pour le débogage
echo "USERNAME: $USERNAME"
echo "PASSWORD: $PASSWORD"
echo "MQTT_BROKER: $MQTT_BROKER"
echo "MQTT_PORT: $MQTT_PORT"
echo "MQTT_USERNAME: $MQTT_USERNAME"
echo "MQTT_PASSWORD: $MQTT_PASSWORD"

python3 /app/veolia/veolia.py
