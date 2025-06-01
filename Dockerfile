# Base Python légère avec Flask et PyYAML
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances
RUN pip install flask pyyaml

# Copier le script Flask
COPY webapp.py /app/webapp.py

# Exposer le port Flask
EXPOSE 5000

# Commande de démarrage
CMD ["python", "webapp.py"]
