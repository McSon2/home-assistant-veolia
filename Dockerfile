FROM python:3.9-slim

# Copiez les fichiers nécessaires dans le conteneur
COPY veolia /app/veolia
COPY run.sh /app/run.sh
COPY config.yaml /app/config.yaml

# Définissez le répertoire de travail
WORKDIR /app

# Installez les dépendances nécessaires
RUN apt-get update && apt-get install -y jq && rm -rf /var/lib/apt/lists/*
RUN pip install requests xmltodict "paho-mqtt<2.0.0"

# Donnez la permission d'exécution au script
RUN chmod +x /app/run.sh

# Commande par défaut à exécuter lors du démarrage du conteneur
CMD ["/app/run.sh"]
