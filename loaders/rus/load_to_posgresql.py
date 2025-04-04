import os
import json
import psycopg2
import pandas as pd
from dotenv import load_dotenv

def database_loader(raw_data):
    
    # Load .env config
    load_dotenv(dotenv_path="../config/.env")

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="housing",
        user="postgres",
        password="strong78361"
    )
    cur = conn.cursor()

    df = raw_data

    # Insert into DB
    for _, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO housing.rus_flat_sale (price, location, seller, date, room, size, house_floor, total_floor)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                row.get("price"),
                row.get("location"),
                row.get("seller"),
                row.get("date"),
                row.get("room"),
                row.get("size"),
                int(row.get("house_floor")) if pd.notnull(row.get("house_floor")) else None,
                row.get("total_floor")
            ))
        except Exception as e:
            print("❌ Skipping invalid row:", row.to_dict())
            print("→ Error:", e)
            conn.rollback()  # rollback current failed INSERT to keep session clean
            continue


    conn.commit()
    cur.close()
    conn.close()

    print("✅ Data inserted into PostgreSQL.")
    print("Connecting to DB:", os.getenv("DB_NAME"), os.getenv("DB_USER"))