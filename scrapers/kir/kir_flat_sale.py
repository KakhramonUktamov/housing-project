import requests
from bs4 import BeautifulSoup
import time

url = "https://www.house.kg/kupit-kvartiru?page={}"

def kir_flat_sale():
    results = []

    try:
        response_page = requests.get(url.format(1), timeout=10)
        response_page.raise_for_status()
        page_soup = BeautifulSoup(response_page.content, "html.parser")
        page_max = int(page_soup.find_all("a", class_="page-link")[-1]['data-page'])
    except:
        page_max = 25

    for page in range(1, page_max):
        try:
            response = requests.get(url.format(page), timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            cards = soup.find_all("div", class_="listing")
        except:
            continue

        for card in cards:
            try:
                price = card.find("div", class_="price").get_text(strip=True)
                title = card.find("p", class_="title").get_text(strip=True)
                location = card.find("div", class_="address").get_text(strip=True)
                date = card.find("div", class_="additional-info").get_text(strip=True)
                link = card.find("p", class_="title").find('a')['href']

                result = {
                    "price_info": price,
                    "title": title,
                    "location_hs": location,
                    "date": date,
                    "link": f"https://www.house.kg{link}"
                }

                results.append(result)
            except:
                continue

        time.sleep(1)

    print("Scraping kir_flat_sale completed successfully.")
    return results





