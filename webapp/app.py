from flask import Flask
import psycopg2
import os

app = Flask(__name__)
DB_HOST = os.environ.get('DB_HOST', 'db')
POSTGRES_DB = os.environ.get('POSTGRES_DB','db_meteo')
POSTGRES_USER = os.environ.get('POSTGRES_USER','user_meteo')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD','password123!')

def get_data():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT ville, temperature, date FROM mesures ORDER BY date DESC LIMIT 10;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.route('/')
def index():
    data = get_data()
    html = "<h1>Dernières mesures météo</h1><ul>"
    for row in data:
        html += f"<li>{row[2]} - {row[0]} : <b>{row[1]}°C</b></li>"
    html += "</ul>"
    return html

if __name__ == '__main__':
    # Important : host='0.0.0.0' pour que l'app soit accessible hors du conteneur
    app.run(host='0.0.0.0', port=80)