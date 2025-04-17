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

def type_clean(text):
    if not text or not isinstance(text, str):
        return None
    return text.split(",")[0].strip() or None


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

def date_clean(text, reference_date=None):
    if not text:
        return None

    now = reference_date or datetime.now()
    text = text.lower().strip()

    if "сегодня" in text:
        return now.date()
    elif "вчера" in text:
        return (now - timedelta(days=1)).date()
    elif "только что" in text:
        return now.date()
    elif "месяц назад" in text or "прошлый месяц" in text:
        month = now.month - 1 or 12
        year = now.year if now.month > 1 else now.year - 1
        return datetime(year, month, 1).date()

    match = re.search(r"(\d+)\s+(минут|час|день|дня|дней|недел[ьяи]|месяц|месяцев|год|года|лет)\s+назад", text)
    if match:
        num = int(match.group(1))
        unit = match.group(2)

        if "минут" in unit:
            delta = timedelta(minutes=num)
        elif "час" in unit:
            delta = timedelta(hours=num)
        elif "день" in unit or "дня" in unit or "дней" in unit:
            delta = timedelta(days=num)
        elif "недел" in unit:
            delta = timedelta(weeks=num)
        elif "месяц" in unit:
            delta = timedelta(days=30 * num)
        elif "год" in unit or "лет" in unit:
            delta = timedelta(days=365 * num)
        else:
            return None

        return (now - delta).date()

    return None


def taj_office_sale_clean(raw_data):
    df = pd.DataFrame(raw_data)

    df['price'] = df['price_info'].apply(price_clean)
    df['type'] = df['title'].apply(type_clean)
    df['size'] = df['title'].apply(size_clean)
    df['date'] = df['date'].apply(date_clean)
    df['currency'] = df['price_info'].apply(currency_clean)
    df['scrape_date'] = datetime.now().date()
    df = df.drop(["title", "price_info"], axis=1)
    
    return df
