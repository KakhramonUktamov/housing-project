from itertools import product
import requests
from bs4 import BeautifulSoup

url_template = "https://www.olx.uz/nedvizhimost/kvartiry/prodazha/{location}/?currency=UYE&page={page}&search%5Border%5D=created_at:desc&search%5Bfilter_float_number_of_rooms:from%5D={room}&search%5Bfilter_enum_type_of_market%5D%5B0%5D={type}&view=list"

property_type = ['primary', 'secondary']
locations = ['tashkent', "toshkent-oblast", "andizhanskaya-oblast", "buharskaya-oblast", "dzhizakskaya-oblast",
             "karakalpakstan", "kashkadarinskaya-oblast", "navoijskaya-oblast", "namanganskaya-oblast",
             "samarkandskaya-oblast", "surhandarinskaya-oblast", "syrdarinskaya-oblast", "ferganskaya-oblast",
             "horezmskaya-oblast"]

rooms = [1, 2, 3, 4, 5]
pages = range(1, 26)

page_links = [
    url_template.format(location=loc, page=pg, room=rm, type=tp)
    for loc, pg, rm, tp in product(locations, pages, rooms, property_type)
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}


def uzb_flat_sale():
    flat_links = []

    for page_link in page_links[:2]:  # test with first 2 for now
        response = requests.get(page_link, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        cards = soup.find_all("div", class_="css-l9drzq")
        for card in cards:
            link_tag = card.find("a", class_="css-1tqlkj0")
            if not link_tag:
                continue

            flat_url = "https://www.olx.uz{}".format(link_tag['href'])

            loc_tag = soup.find("p", class_="css-vbz67q")
            loc_text = loc_tag.get_text(strip=True) if loc_tag else None

            flat_links.append({
                "flat": flat_url,
                "location": loc_text
            })

    results = []

    for item in flat_links:
        flat = item["flat"]
        location = item["location"]

        response = requests.get(flat, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        title = [i.text for i in soup.find_all("p", class_="css-1los5bp")]

        price_div = soup.find("div", class_="css-e2ir3r")
        price = price_div.get_text(strip=True) if price_div else None

        results.append({
            "title": title,
            "price": price,
            "loc": location
        })

    return results
