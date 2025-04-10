import os
import psycopg2
from dotenv import load_dotenv

def taj_office_sale_loader(raw_data):
    
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
                INSERT INTO housing.taj_office_sale (price, date, location, type, size, scrape_date)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                row.get("price"),
                row.get("date"),
                row.get("location"),
                row.get("type"),
                row.get("size"),
                row.get("scrape_date")
            ))
        except Exception as e:
            print("❌ Failed row:")
            print(row.to_dict())
            print("→ Error:", e)



    conn.commit()
    cur.close()
    conn.close()

    print("✅ Data inserted into PostgreSQL.")
    print("Connecting to DB:", os.getenv("DB_NAME"), os.getenv("DB_USER"))