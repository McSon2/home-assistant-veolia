import json
import os
from veolia_client import VeoliaClient

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Afficher les variables d'environnement pour le débogage
print(f"USERNAME: {username}")
print(f"PASSWORD: {password}")

#client = VeoliaClient(email="maximesaltet@gmail.com", password="Happy.Fifi@1994")
client = VeoliaClient(email=username, password=password)

# Se connecter
try:
    client.login()
    print("Connexion réussie")
except Exception as e:
    print(f"Erreur de connexion: {e}")

# Récupérer les données de consommation journalière
try:
    data_daily = client.update(month=False)
    print("Données de consommation journalière :")
    #print(data_daily)
    print(json.dumps({"history": data_daily}, default=str))
except Exception as e:
    print(f"Erreur lors de la récupération des données journalières: {e}")

# Récupérer les données de consommation mensuelle
try:
    data_monthly = client.update(month=True)
    print("Données de consommation mensuelle :")
    #print(data_monthly)
    print(json.dumps({"history": data_monthly}, default=str))
except Exception as e:
    print(f"Erreur lors de la récupération des données mensuelles: {e}")
