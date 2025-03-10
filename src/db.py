import os
import psycopg2

db = None
try:
    # Establish the connection
    db = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    print("Connected to database.")
except psycopg2.Error as e:
    print("Error connecting to the database:", e)