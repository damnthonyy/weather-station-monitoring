FROM python:3.9-slim

WORKDIR /app

# On installe Flask et le connecteur PostgreSQL
RUN pip install flask psycopg2-binary

COPY app.py .

# On expose le port 80 à l'intérieur du conteneur
EXPOSE 80

# On lance l'app en précisant qu'elle doit écouter sur le port 80
CMD ["python", "app.py"]