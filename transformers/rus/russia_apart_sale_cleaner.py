import pandas as pd
import re
from datetime import datetime


def clean_room(text):
    # Number of rooms
    if "студия" in text.lower():
        rooms = 0
    else:
        room_match = re.search(r"(\d+)-к", text)
        rooms = int(room_match.group(1)) if room_match else None
    return rooms 

def clean_size(text):
    size_match = re.search(r"(\d+(\.\d+)?)\s?м²", text)
    size = float(size_match.group(1)) if size_match else None
    return size

def clean_house_floor(text):
    floor_match = re.search(r"(\d+)[/\\](\d+)", text)
    current_floor = int(floor_match.group(1)) if floor_match else None
    return current_floor

def clean_total_floor(text):
    floor_match = re.search(r"(\d+)[/\\](\d+)", text)
    total_floors = int(floor_match.group(2) if floor_match else None)
    return total_floors

def clean_price(price_str):
    
    return int(re.sub(r"[^\d]","", price_str)) if price_str else None

def clean_date(date_str):
    if "час" in date_str:
        return pd.Timestamp.today().strftime("%Y-%m-%d")
    elif "Вчера" in date_str:
        return (pd.Timestamp.today() - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        return date_str.strip()  # or parse with dateparser


def clean_location(text):
    loc = text.split(',')[0].strip() if text else None
    
    replacements = {
        "обл.": "область",
        "респ.": "республика",
        "край.": "край",
        "г.": "",
    }

    for short, full in replacements.items():
        loc = loc.replace(short, full)

    return loc



def clean_data(raw_data):
    df = pd.DataFrame(raw_data)
    df['room'] = df['title'].apply(clean_room)
    df['size'] = df['title'].apply(clean_size)
    df["price"] = df["price"].apply(clean_price)
    df['house_floor'] = df['title'].apply(clean_house_floor)
    df['total_floor'] = df['title'].apply(clean_total_floor)
    df["date"] = df["date"].apply(clean_date)
    df["location"] = df["location"].apply(clean_location)
    df['scrape_date'] = datetime.now().date()
    df = df.drop("title", axis=1)
    return df

