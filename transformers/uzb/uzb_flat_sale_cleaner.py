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
    

MONTHS_RU = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12
}

def date_clean(info: str, current_date: datetime = None) -> tuple:
    
    text = re.split(r"\s*-\s*", info)[1].strip()
  
    
    if current_date is None:
        current_date = datetime.now()

    text = text.strip().lower()

    if "сегодня" in text:
        return datetime(current_date.year, current_date.month, current_date.day).date()

    elif "вчера" in text:
        dt = current_date - timedelta(days=1)
        return datetime(dt.year, dt.month, dt.day).date()

    # Full date with year: 11 апреля 2025 г.
    match = re.match(r'(\d{1,2})\s([а-я]+)\s(\d{4})', text)
    if match:
        day, month_str, year = match.groups()
        month = MONTHS_RU.get(month_str)
        if month:
            return datetime(int(year), month, int(day)).date()

    # Partial date without year: 11 апреля
    match = re.match(r'(\d{1,2})\s([а-я]+)', text)
    if match:
        day, month_str = match.groups()
        month = MONTHS_RU.get(month_str)
        if month:
            return datetime(current_date.year, month, int(day)).date()

    return None

def size_clean(info_list):
    for item in info_list:
        if "общая площадь" in item.lower():
            try:
                return float(item.split(":")[1].strip())
            except:
                return None
    return None

def room_clean(info_list):
    for item in info_list:
        if "количество комнат" in item.lower():
            try:
                return int(item.split(":")[1].strip())
            except:
                return None
    return None

def floor_clean(info_list):
    for item in info_list:
        if item.lower().startswith("этаж:"):
            try:
                return int(item.split(":")[1].strip())
            except:
                return None
    return None

def house_floor(info_list):
    for item in info_list:
        if "этажность дома" in item.lower():
            try:
                return int(item.split(":")[1].strip())
            except:
                return None
    return None

def location_clean(text):
    if not text:
        return None
    try:
        return re.split(r"\s*-\s*", text)[0].strip()
    except Exception:
        return None


def uzb_flat_sale_clean(raw_data):
    df = pd.DataFrame(raw_data)

    df['price'] = df['price'].apply(price_clean)
    df['room'] = df['title'].apply(room_clean)
    df['location'] = df['loc'].apply(location_clean)
    df['house_floor'] = df['title'].apply(floor_clean)
    df['total_floor'] = df['title'].apply(house_floor)
    df['size'] = df['title'].apply(size_clean)
    df['date'] = df['loc'].apply(date_clean)
    df['scrape_date'] = datetime.now().date()
    df = df.drop(["title","loc"], axis=1)
    
    return df
