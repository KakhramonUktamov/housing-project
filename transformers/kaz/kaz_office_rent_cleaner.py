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

# Mapping for Russian short months
RU_MONTHS = {
    "янв": 1, "фев": 2, "мар": 3, "апр": 4,
    "май": 5, "июн": 6, "июл": 7, "авг": 8,
    "сен": 9, "окт": 10, "ноя": 11, "дек": 12
}

def date_clean(text, reference_date=None):
    if not text:
        return None

    now = reference_date or datetime.now()
    text = text.lower().strip()

    # Today / yesterday / just now
    if "сегодня" in text:
        return now.date()
    elif "вчера" in text:
        return (now - timedelta(days=1)).date()
    elif "только что" in text:
        return now.date()

    # Relative time like "3 дня назад"
    match = re.search(r"(\d+)\s+(минут|час|день|дня|дней|недел[ьяи]|месяц|месяцев|год|года|лет)\s+назад", text)
    if match:
        num = int(match.group(1))
        unit = match.group(2)

        if "минут" in unit:
            delta = timedelta(minutes=num)
        elif "час" in unit:
            delta = timedelta(hours=num)
        elif any(u in unit for u in ["день", "дня", "дней"]):
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

    # Absolute Russian date like "3 апр." or "28 мар."
    match = re.search(r"(\d{1,2})\s+([а-я]{3})\.", text)
    if match:
        day = int(match.group(1))
        month_abbr = match.group(2)
        month = RU_MONTHS.get(month_abbr)
        if month:
            return datetime(now.year, month, day).date()

    return None


def kaz_office_rent_clean(raw_data):
    df = pd.DataFrame(raw_data)

    df['price'] = df['price_info'].apply(price_clean)
    df['size'] = df['title'].apply(size_clean)
    df['date'] = df['date'].apply(date_clean)
    df['currency'] = df['price_info'].apply(currency_clean)
    df['scrape_date'] = datetime.now().date()
    df = df.drop(["title", "price_info"], axis=1)
    
    return df