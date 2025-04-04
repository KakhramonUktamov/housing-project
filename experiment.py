import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


def price_clean(text):
    if not text:
        return None
    try:
        return int(re.sub(r"[^\d]", "", text))
    except ValueError:
        return None
    
url = "https://krisha.kz/prodazha/kommercheskaya-nedvizhimost/typi-ofisy/?page={}"



page = requests.get(url.format(1))
page_soup = BeautifulSoup(page.content, "html.parser")
n_pages = int(page_soup.find_all("a", class_="paginator__btn")[-2].get_text(strip=True))
   
flats = [url.format(i) for i in range(1, n_pages if n_pages else 2)]
    
results = []


response = requests.get(flats[2])
soup = BeautifulSoup(response.content, "html.parser")

cards = soup.find_all("div", class_="a-card__inc")

price_cards = [card.find("div", class_="a-card__price") for card in cards]
price = [price_card.get_text(separator="|", strip=True).split("|")[0] for price_card in price_cards]

    