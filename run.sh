#!/usr/bin/env bash
CONFIG_PATH=/data/options.json

USERNAME=$(jq --raw-output '.username' $CONFIG_PATH)
PASSWORD=$(jq --raw-output '.password' $CONFIG_PATH)
MQTT_BROKER=$(jq --raw-output '.mqtt_broker' $CONFIG_PATH)
MQTT_PORT=$(jq --raw-output '.mqtt_port' $CONFIG_PATH)
MQTT_USERNAME=$(jq --raw-output '.mqtt_username' $CONFIG_PATH)
MQTT_PASSWORD=$(jq --raw-output '.mqtt_password' $CONFIG_PATH)
HASS_HOST=$(jq --raw-output '.hass_host' $CONFIG_PATH)
HASS_TOKEN=$(jq --raw-output '.hass_token' $CONFIG_PATH)

export USERNAME
export PASSWORD
export MQTT_BROKER
export MQTT_PORT
export MQTT_USERNAME
export MQTT_PASSWORD
export HASS_HOST
export HASS_TOKEN

# Afficher les variables d'environnement pour le débogage
#echo "USERNAME: $USERNAME"
#echo "PASSWORD: $PASSWORD"
#echo "MQTT_BROKER: $MQTT_BROKER"
#echo "MQTT_PORT: $MQTT_PORT"
#echo "MQTT_USERNAME: $MQTT_USERNAME"
#echo "MQTT_PASSWORD: $MQTT_PASSWORD"
#echo "HASS_HOST: $HASS_HOST"
#echo "HASS_TOKEN: $HASS_TOKEN"

# Fonction pour calculer le temps jusqu'à la prochaine exécution à 17h36
calculate_sleep_duration() {
    current_time=$(date +%s)
    target_time=$(date -d "17:36:00" +%s)
    if [ "$current_time" -gt "$target_time" ]; then
        target_time=$((target_time + 24 * 60 * 60))
    fi
    sleep_duration=$((target_time - current_time))
}

# Boucle infinie pour exécuter le script Python à 17h36 chaque jour
while true; do
    calculate_sleep_duration
    echo "Sleeping for $sleep_duration seconds until 17:36..."
    sleep $sleep_duration
    python3 /app/veolia/veolia.py
    echo "Script exécuté à $(date)"
done
