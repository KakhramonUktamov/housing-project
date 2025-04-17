import requests
from bs4 import BeautifulSoup
import time

url = "https://krisha.kz/prodazha/kvartiry/?page={}"

def kaz_flat_sale():
    results = []

    try:
        page = requests.get(url.format(1), timeout=10)
        page.raise_for_status()
        page_soup = BeautifulSoup(page.content, "html.parser")
        n_pages = int(page_soup.find_all("a", class_="paginator__btn")[-2].get_text(strip=True))
    except:
        n_pages = 2

    flats = [url.format(i) for i in range(1, n_pages if n_pages else 2)]

    for page in flats:
        try:
            response = requests.get(page, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            cards = soup.find_all("div", class_="a-card a-storage-live ddl_product ddl_product_link not-colored is-visible")
        except:
            continue

        for card in cards:
            try:
                price = card.find("div", class_="a-card__price").get_text(strip=True).split("за")[0]
                title = card.find("div", class_="a-card__header-left").get_text()
                location = [i.get_text(strip=True) for i in card.find_all("div", class_="a-card__stats-item")][0]
                date = [i.get_text(strip=True) for i in card.find_all("div", class_="a-card__stats-item")][1]
                result = {
                    "price_info": price,
                    "title": title,
                    "location": location,
                    "date": date
                }
                results.append(result)
            except:
                continue

        time.sleep(1)

    print("Scraping kaz_flat_sale completed successfully.")
    return results





