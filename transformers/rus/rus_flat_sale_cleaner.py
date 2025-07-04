import pandas as pd
import re
from datetime import datetime
import dateparser
from transformers.currency_utils import get_currency

currency=get_currency("USD","RUB")

def clean_room(text):
    if not text:
        return None
    if "студия" in text.lower():
        return 0
    match = re.search(r"(\d+)-к", text)
    return int(match.group(1)) if match else None


def clean_size(text):
    if not text:
        return None
    try:
        # Normalize text (replace commas with dots, and handle different square meter symbol)
        text = text.replace(",", ".").replace("\xa0", " ").replace("\u202f", " ")
        match = re.search(r"(\d+(?:\.\d+)?)\s*(м²|м2)", text, re.IGNORECASE)
        return float(match.group(1)) if match else None
    except Exception:
        return None


def clean_house_floor(text):
    if not text:
        return None
    match = re.search(r"(\d+)[/\\](\d+)", text)
    return int(match.group(1)) if match else None


def clean_total_floor(text):
    if not text:
        return None
    match = re.search(r"(\d+)[/\\](\d+)", text)
    return int(match.group(2)) if match else None


def clean_price(text):
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

def rus_flat_sale_clean(raw_data):
    df = pd.DataFrame(raw_data)
    df['room'] = df['title'].apply(clean_room)
    df['size'] = df['title'].apply(clean_size)
    df['price'] = round(df['price_info'].apply(clean_price)/currency, 2)
    df['currency'] = df['price_info'].apply(clean_currency)
    df['house_floor'] = df['title'].apply(clean_house_floor)
    df['total_floor'] = df['title'].apply(clean_total_floor)
    df['date'] = df['date'].apply(clean_date)
    df['location'] = df['location'].apply(clean_location)
    df['scrape_date'] = datetime.now().date()
    df.drop(columns=['title',"price_info"], inplace=True, errors='ignore')
    df = remove_outliers(df, ['price', 'size', 'house_floor', 'total_floor'])
    df = df[(df['room'] >= 1) & (df['room'] <= 6)]
    df = df.drop_duplicates()

    return df
