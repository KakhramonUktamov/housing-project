import os
import psycopg2
from dotenv import load_dotenv
import math
from pathlib import Path

def clean_value(val):
    if isinstance(val, float) and math.isnan(val):
        return None
    return val

def uzb_office_sale_loader(raw_data):
    
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
            cleaned = {k: clean_value(v) for k, v in row.to_dict().items()}

            cur.execute("""
                INSERT INTO housing.uzb_office_sale (price, date, location, house_floor, total_floor, size, currency, scrape_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                cleaned["price"],
                cleaned["date"],
                cleaned["location"],
                cleaned["house_floor"],
                cleaned["total_floor"],
                cleaned["size"],
                cleaned["currency"],
                cleaned["scrape_date"]
            ))

        except Exception as e:
            print("Failed row:")
            print(row.to_dict())
            print("Error:", e)
            conn.rollback()




    conn.commit()
    cur.close()
    conn.close()

    print("Data inserted into PostgreSQL.")
    print("Connecting to DB:", os.getenv("DB_NAME"), os.getenv("DB_USER"))