import pandas as pd
import re
from datetime import datetime, timedelta


def price_clean(text):
    if not text:
        return None
    try:
        return int(re.sub(r"[^\d]", "", text))
    except ValueError:
        return None
    
def currency_clean(text):
    if not text:
        return None
    match = re.search(r"[^\d\s]+", text)
    return match.group(0) if match else None

def room_clean(text):
    match = re.search(r"(\d+)-комн", text)
    return int(match.group(1)) if match else None

def floor_clean(text):
    floor_match = re.search(r"(\d+)\s*этаж", text)
    return int(floor_match.group(1)) if floor_match else None

def total_floor(text):
    match = re.search(r"этаж\s+из\s+(\d+)", text)
    return int(match.group(1)) if match else None


def size_clean(text):
    if not text:
        return None
    try:
        # Normalize text (replace commas with dots, and handle different square meter symbols)
        text = text.replace(",", ".").replace("\xa0", " ").replace("\u202f", " ")
        match = re.search(r"(\d+(?:\.\d+)?)\s*(м²|м2)", text, re.IGNORECASE)
        return float(match.group(1)) if match else None
    except Exception:
        return None

def location_clean(text):
    if not text:
        return None
    return text.split(',')[0].strip()


def date_clean(text, reference_time=None):
    if not text:
        return None

    now = reference_time or datetime.now()
    text = text.lower().strip()

    # Match formats like "2 часа назад", "5 дней назад", etc.
    match = re.search(r"(\d+)\s+(секунд|минут|час|день|дня|дней|недел[яьи]?|месяц|месяцев|лет|год[а]?)\s+назад", text)
    if match:
        num = int(match.group(1))
        unit = match.group(2)

        if "секунд" in unit:
            delta = timedelta(seconds=num)
        elif "минут" in unit:
            delta = timedelta(minutes=num)
        elif "час" in unit:
            delta = timedelta(hours=num)
        elif "день" in unit or "дня" in unit or "дней" in unit:
            delta = timedelta(days=num)
        elif "недел" in unit:
            delta = timedelta(weeks=num)
        elif "месяц" in unit:
            delta = timedelta(days=30 * num)  # Approximate
        elif "год" in unit or "лет" in unit:
            delta = timedelta(days=365 * num)  # Approximate
        else:
            return None

        # Return formatted as YYYY-MM-DD
        return (now - delta).date()

    return None



def kir_flat_sale_clean(raw_data):
    df = pd.DataFrame(raw_data)

    df['price'] = df['price_info'].apply(price_clean)
    df['room'] = df['title'].apply(room_clean)
    df['house_floor'] = df['title'].apply(floor_clean)
    df['total_floor'] = df['title'].apply(total_floor)
    df['size'] = df['title'].apply(size_clean)
    df['location'] = df['location_hs'].apply(location_clean)
    df['date'] = df['date'].apply(date_clean)
    df['currency'] = df['price_info'].apply(currency_clean)
    df['scrape_date'] = datetime.now().date()
    df = df.drop(["title","location_hs","price_info"], axis=1)
    
    return df
