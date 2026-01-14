import psycopg2
import random
import time
import os

DB_HOST = os.environ.get('DB_HOST','localhost')
POSTGRES_DB = os.environ.get('POSTGRES_DB','db_meteo')
POSTGRES_USER = os.environ.get('POSTGRES_USER','user_meteo')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD','password123!')

def connect_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD
            )
            return conn
        except Exception as e:
            print("Error connecting to database: ", e)
            time.sleep(2)
conn = connect_db()
cur = conn.cursor()

## create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS mesures (id SERIAL PRIMARY KEY, ville TEXT, temperature FLOAT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)""")
conn.commit()
print("Table created successfully")

while True:
    temp = round(random.uniform(10, 20), 2)
    cur.execute("INSERT INTO mesures (ville, temperature) VALUES (%s, %s)", ("Paris", temp))
    conn.commit()
    print(f"Data inserted successfully: {temp}°C")
    time.sleep(10)


