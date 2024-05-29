import json
import os
from veolia_client import VeoliaClient

os.environ["USERNAME"] = "maximesaltet@gmail.com"
os.environ["PASSWORD"] = "Happy.Fifi@1994"

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Afficher les variables d'environnement pour le débogage
print(f"USERNAME: {username}")
print(f"PASSWORD: {password}")

client = VeoliaClient(email=username, password=password)
try:
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
except Exception as e:
    print(f"Erreur de connexion: {e}")
