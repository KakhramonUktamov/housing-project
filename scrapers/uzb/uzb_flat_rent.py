from itertools import product
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

url_template = "https://www.olx.uz/nedvizhimost/kvartiry/arenda-dolgosrochnaya/{location}/?currency=UYE&page={page}&search%5Bfilter_float_number_of_rooms%3Afrom%5D={room}&search%5Border%5D=created_at%3Adesc"

locations = ['tashkent', "toshkent-oblast", "andizhanskaya-oblast", "buharskaya-oblast", "dzhizakskaya-oblast",
             "karakalpakstan", "kashkadarinskaya-oblast", "navoijskaya-oblast", "namanganskaya-oblast",
             "samarkandskaya-oblast", "surhandarinskaya-oblast", "syrdarinskaya-oblast", "ferganskaya-oblast",
             "horezmskaya-oblast"]

rooms = [1, 2, 3, 4, 5]
pages = range(1, 26)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

page_links = [
    url_template.format(location=loc, page=pg, room=rm)
    for loc, pg, rm in product(locations, pages, rooms)
]


def fetch_listing_links(page_link):
    try:
        response = requests.get(page_link, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        cards = soup.find_all("div", class_="css-l9drzq")
        links = []

        for card in cards:
            link_tag = card.find("a", class_="css-1tqlkj0")
            loc_tag = card.find("p", class_="css-vbz67q")

            if not link_tag:
                continue

            flat_url = "https://www.olx.uz{}".format(link_tag['href'])
            loc_text = loc_tag.get_text(strip=True) if loc_tag else None

            links.append({
                "flat": flat_url,
                "location": loc_text
            })
        return links
    except Exception as e:
        print(f"Error fetching {page_link}: {e}")
        return []


def fetch_listing_details(item):
    try:
        response = requests.get(item["flat"], headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        title = [i.text for i in soup.find_all("p", class_="css-1los5bp")]

        price_div = soup.find("div", class_="css-e2ir3r")
        price = price_div.get_text(strip=True) if price_div else None

        return {
            "title": title,
            "price_info": price,
            "loc": item["location"]
        }
    except Exception as e:
        print(f"Error fetching {item['flat']}: {e}")
        return None


def uzb_flat_rent():
    # Phase 1: Get all listing links concurrently
    flat_links = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for results in executor.map(fetch_listing_links, page_links):  # Adjust slice for testing
            flat_links.extend(results)

    # Phase 2: Fetch all listing details concurrently
    results = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for res in executor.map(fetch_listing_details, flat_links):
            if res:
                results.append(res)

    return results
