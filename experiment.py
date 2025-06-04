import requests
from datetime import datetime
import re
from bs4 import BeautifulSoup

url = "https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To={}"
response = requests.get(url)
data = BeautifulSoup(response.content, 'html.parser')
currency = data.find("p", class_="sc-708e65be-1 chuBHG").get_text()

def extract_numeric_value(price_str: str) -> float:
    number_part = re.findall(r"[\d.,]+", price_str)
    if number_part:
        cleaned = number_part[0].replace(",", "")
        return float(cleaned)
    else:
        return 0.0


