import os
import psycopg2
from dotenv import load_dotenv

def kaz_office_sale_loader(raw_data):
    
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
                INSERT INTO housing.kaz_office_sale (price, date, location, size, currency, scrape_date)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                row.get("price"),
                row.get("date"),
                row.get("location"),
                row.get("size"),
                row.get("currency"),
                row.get("scrape_date")
            ))

        except Exception as e:
            print("Failed row:")
            print(row.to_dict())
            print("→ Error:", e)

    print("Data inserted into PostgreSQL.")
    print("Connecting to DB:", os.getenv("DB_NAME"), os.getenv("DB_USER"))

    conn.commit()
    cur.close()
    conn.close()

    