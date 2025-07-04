import requests
from bs4 import BeautifulSoup
import re

def get_currency(From, To):
    url = f"https://www.xe.com/currencyconverter/convert/?Amount=1&From={From}&To={To}"
    response = requests.get(url)
    data = BeautifulSoup(response.content, 'html.parser')
    currency = data.find("p", class_="sc-56d5cf17-1 ifKLEd").get_text()
    return float(re.sub(r"[^\d.]", "", currency))
