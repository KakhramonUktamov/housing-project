import os
import psycopg2
from dotenv import load_dotenv

def kir_office_sale_loader(raw_data):
    
    # Load .env config
    load_dotenv(dotenv_path="../config/.env")

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host="192.168.14.229",
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
                INSERT INTO housing.kir_office_sale (price, date, location, size, scrape_date, link)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                row.get("price"),
                row.get("date"),
                row.get("location"),
                row.get("size"),
                row.get("scrape_date"),
                row.get("link")
            ))

        except Exception as e:
            print("❌ Failed row:")
            print(row.to_dict())
            print("→ Error:", e)

    print("✅ Data inserted into PostgreSQL.")
    print("Connecting to DB:", os.getenv("DB_NAME"), os.getenv("DB_USER"))

    conn.commit()
    cur.close()
    conn.close()

    