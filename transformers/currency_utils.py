import requests
from bs4 import BeautifulSoup
import re

def get_currency(From, To):
    url = f"https://www.xe.com/currencyconverter/convert/?Amount=1&From={From}&To={To}"
    response = requests.get(url)
    data = BeautifulSoup(response.content, 'html.parser')
    currency = data.find("p", class_="sc-708e65be-1 chuBHG").get_text()
    return float(re.sub(r"[^\d.]", "", currency))
