import requests
from bs4 import BeautifulSoup

url = "https://krisha.kz/arenda/kvartiry/?page={}"

def kaz_flat_rent():

    page = requests.get(url.format(1))
    page_soup = BeautifulSoup(page.content, "html.parser")
    n_pages = int(page_soup.find_all("a", class_="paginator__btn")[-2].get_text(strip=True))

    
    flats = [url.format(i) for i in range(1, n_pages if n_pages else 2)]
    
    results = []

    for page in flats[:3]:
        response = requests.get(page)
        soup = BeautifulSoup(response.content, "html.parser")

        cards = soup.find_all("div", class_="a-card a-storage-live ddl_product ddl_product_link not-colored is-visible")

        for card in cards:

            price = card.find("div", class_="a-card__price").get_text(strip=True)
            title = card.find("div", class_="a-card__header-left").get_text()
            location = [i.get_text(strip=True) for i in card.find_all("div", class_="a-card__stats-item")][0]
            date = [i.get_text(strip=True) for i in card.find_all("div", class_="a-card__stats-item")][1]
            result = {
                "price": price,
                "title": title,
                "location": location,
                "date": date
            }
            results.append(result)

    return results