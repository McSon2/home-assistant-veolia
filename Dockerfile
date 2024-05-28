FROM python:3.9-slim

# Copiez les fichiers nécessaires dans le conteneur
COPY veolia /app/veolia
COPY run.sh /app/run.sh
COPY config.json /app/config.json

# Définissez le répertoire de travail
WORKDIR /app

# Installez les dépendances nécessaires
RUN pip install requests

# Donnez la permission d'exécution au script
RUN chmod +x /app/run.sh

# Commande par défaut à exécuter lors du démarrage du conteneur
CMD ["/app/run.sh"]
