import pandas as pd
import re
from datetime import datetime
import dateparser
from transformers.currency_utils import get_currency

currency=get_currency("USD","RUB")

def clean_size(text):
    if not text:
        return None
    try:
        # Normalize text (replace commas with dots, and handle different square meter symbols)
        text = text.replace(",", ".").replace("\xa0", " ").replace("\u202f", " ")
        match = re.search(r"(\d+(?:\.\d+)?)\s*(м²|м2)", text, re.IGNORECASE)
        return float(match.group(1)) if match else None
    except Exception:
        return None

def clean_price(text):
    if not text:
        return None
    try:
        return int(re.sub(r"[^\d]", "", text))
    except ValueError:
        return None

def clean_price_sqm(text):
    if not text:
        return None
    try:
        return int(re.sub(r"[^\d]", "", text))
    except ValueError:
        return None
    
def clean_currency(text):
    if not text:
        return None
    match = re.search(r"[^\d\s]+", text)
    return match.group(0) if match else None


def clean_date(text):
    if not text:
        return None
    parsed = dateparser.parse(text, settings={'PREFER_DATES_FROM': 'past'})
    return parsed.date().isoformat() if parsed else text.strip()


def clean_location(text):
    if not text:
        return None
    loc = text.split(',')[0].strip()
    replacements = {
        "обл.": "область",
        "респ.": "республика",
        "край.": "край",
        "г.": "",
    }
    for short, full in replacements.items():
        loc = loc.replace(short, full)
    return loc

def remove_outliers(df, columns):
    for column in columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return df

def rus_office_sale_clean(raw_data):
    df = pd.DataFrame(raw_data)
    df['price'] = round(df['price_info'].apply(clean_price)/currency, 2)
    df['price_sqm'] = df['price_sqm'].apply(clean_price_sqm)
    df['size'] = df['price']/df['price_sqm']
    df['currency'] = df['price_info'].apply(clean_currency)
    df['date'] = df['date'].apply(clean_date)
    df['location'] = df['location'].apply(clean_location)
    df['scrape_date'] = datetime.now().date()
    df.drop(columns=['title',"price_info","price_sqm"], inplace=True, errors='ignore')
    df = remove_outliers(df, ['price', 'size'])
    df = df.drop_duplicates()

    return df
