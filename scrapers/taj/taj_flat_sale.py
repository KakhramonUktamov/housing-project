from bs4 import BeautifulSoup
import pandas as pd
import requests

url = "https://somon.tj/nedvizhimost/prodazha-kvartir/?page={}"


def taj_flat_sale():

    results = []

    page = requests.get(url.format(1))
    page_soup = BeautifulSoup(page.content, 'html.parser')
    max_page=page_soup.find_all("a", class_="page-number js-page-filter")[-1].text

    flat_pages = [url.format(index) for index in range(1, int(max_page))]

    for page in flat_pages:

        response = requests.get(page)
        soup = BeautifulSoup(response.content, "html.parser")
        cards = soup.find_all("div", class_="advert js-item-listing")

        for card in cards:
            price = card.find("div", class_="advert__content-header").get_text().split(".")[0]
            title = card.find("a", class_="advert__content-title").get_text()
            date = card.find("div", class_="advert__content-date").get_text()
            location = card.find("div", class_="advert__content-place").get_text()

            result={
                "price": price,
                "title": title,
                "date": date,
                "location": location
            }
            results.append(result)

    return results

