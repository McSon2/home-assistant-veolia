#!/usr/bin/env bash
export USERNAME="votre_email"
export PASSWORD="votre_mot_de_passe"

# Afficher les variables d'environnement pour le débogage
echo "USERNAME: $USERNAME"
echo "PASSWORD: $PASSWORD"

python3 /app/veolia/veolia.py
