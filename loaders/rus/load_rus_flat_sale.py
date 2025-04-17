import os
import json
import psycopg2
import pandas as pd
from dotenv import load_dotenv

def rus_flat_sale_loader(raw_data):
    
    # Load .env config
    load_dotenv(dotenv_path="config/.env")

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    cur = conn.cursor()

    df = raw_data

    # Insert into DB
    for _, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO housing.rus_flat_sale (price, location, date, room, size, house_floor, total_floor, currency, scrape_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                row.get("price"),
                row.get("location"),
                row.get("date"),
                row.get("room"),
                row.get("size"),
                row.get("house_floor"),
                row.get("total_floor"),
                row.get("currency"),
                row.get("scrape_date")
            ))
        except Exception as e:
            print("Skipping invalid row:", row.to_dict())
            print("Error:", e)
            conn.rollback()  # rollback current failed INSERT to keep session clean
            continue


    conn.commit()
    cur.close()
    conn.close()

    print("Data inserted into PostgreSQL.")
    print("Connecting to DB:", os.getenv("DB_NAME"), os.getenv("DB_USER"))