import os
import json
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

def rus_office_rent_loader(raw_data):
    
    # Load .env config
    load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / "config" / ".env")

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
                INSERT INTO housing.rus_office_rent (price, location, date, size, currency, scrape_date)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                row.get("price"),
                row.get("location"),
                row.get("date"),
                row.get("size"),
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