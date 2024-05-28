#!/usr/bin/env bash
CONFIG_PATH=/data/options.json

USERNAME=$(jq --raw-output '.username' $CONFIG_PATH)
PASSWORD=$(jq --raw-output '.password' $CONFIG_PATH)

export USERNAME
export PASSWORD

# Afficher les variables d'environnement pour le débogage
echo "USERNAME: $USERNAME"
echo "PASSWORD: $PASSWORD"

python3 /app/veolia/veolia.py
