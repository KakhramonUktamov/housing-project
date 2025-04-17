from bs4 import BeautifulSoup
import time
import requests

url = "https://somon.tj/nedvizhimost/prodazha-kvartir/?page={}"

def taj_flat_sale():
    results = []

    try:
        page = requests.get(url.format(1), timeout=10)
        page.raise_for_status()
        page_soup = BeautifulSoup(page.content, 'html.parser')
        max_page = int(page_soup.find_all("a", class_="page-number js-page-filter")[-1].text)
    except:
        max_page = 1

    flat_pages = [url.format(index) for index in range(1, max_page + 1)]

    for page_url in flat_pages:
        try:
            response = requests.get(page_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            cards = soup.find_all("div", class_="advert js-item-listing")
        except:
            continue

        for card in cards:
            try:
                price = card.find("div", class_="advert__content-header").get_text(strip=True).split(".")[0]
                title = card.find("a", class_="advert__content-title").get_text(strip=True)
                date = card.find("div", class_="advert__content-date").get_text(strip=True)
                location = card.find("div", class_="advert__content-place").get_text(strip=True)

                result = {
                    "price_info": price,
                    "title": title,
                    "date": date,
                    "location": location
                }
                results.append(result)
            except:
                continue

        time.sleep(1)

    print("Scraping completed successfully.")
    return results

