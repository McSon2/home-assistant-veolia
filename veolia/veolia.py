import json
from veolia_client import VeoliaClient
import os

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

client = VeoliaClient(email=username, password=password)
if client.login():
    print("Connexion réussie")
    try:
        daily_data = client.update(month=False)
        print("Données de consommation journalière :")
        print(json.dumps({"history": daily_data}, default=str))
    except Exception as e:
        print(f"Erreur lors de la récupération des données journalières: {e}")

    try:
        monthly_data = client.update(month=True)
        print("Données de consommation mensuelle :")
        print(json.dumps({"history": monthly_data}, default=str))
    except Exception as e:
        print(f"Erreur lors de la récupération des données mensuelles: {e}")
else:
    print("Erreur de connexion")
