# 1. On part d'une image légère de Python
FROM python:3.9-slim

# 2. On définit le dossier de travail dans le conteneur
WORKDIR /app

# 3. On installe la bibliothèque pour se connecter à PostgreSQL
RUN pip install psycopg2-binary

# 4. On copie notre script dans le conteneur
COPY main.py .

# 5. La commande qui lance le script
CMD ["python", "main.py"]