#!/usr/bin/env bash

# Utilisation de bashio pour récupérer les options de configuration
USERNAME=$(bashio::config 'username')
PASSWORD=$(bashio::config 'password')

export USERNAME
export PASSWORD

# Afficher les variables d'environnement pour le débogage
echo "USERNAME: $USERNAME"
echo "PASSWORD: $PASSWORD"

python3 /app/veolia/veolia.py
