from itertools import product
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

url_template = "https://www.olx.uz/nedvizhimost/kvartiry/prodazha/{location}/?currency=UYE&page={page}&search%5Border%5D=created_at:desc&search%5Bfilter_float_number_of_rooms:from%5D={room}&search%5Bfilter_enum_type_of_market%5D%5B0%5D={type}&view=list"

property_type = ['primary', 'secondary']
locations = ["toshkent-oblast", "andizhanskaya-oblast", "buharskaya-oblast", "dzhizakskaya-oblast",
             "karakalpakstan", "kashkadarinskaya-oblast", "navoijskaya-oblast", "namanganskaya-oblast",
             "samarkandskaya-oblast", "surhandarinskaya-oblast", "syrdarinskaya-oblast", "ferganskaya-oblast",
             "horezmskaya-oblast"]

rooms = [1, 2, 3, 4, 5]
pages = range(1, 6)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

page_links = [
    url_template.format(location=loc, page=pg, room=rm, type=tp)
    for loc, pg, rm, tp in product(locations, pages, rooms, property_type)
]


def get_flat_links(page_link):
    flat_links = []
    try:
        response = requests.get(page_link, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")

        cards = soup.find_all("div", class_="css-l9drzq")
        for card in cards:
            link_tag = card.find("a", class_="css-1tqlkj0")
            loc_tag = card.find("p", class_="css-vbz67q")

            if link_tag:
                flat_url = "https://www.olx.uz{}".format(link_tag['href'])
                location = loc_tag.get_text(strip=True) if loc_tag else None
                flat_links.append({
                    "flat": flat_url,
                    "location": location
                })
    except Exception as e:
        print(f"Error getting page {page_link}: {e}")
    return flat_links

def scrape_flat_details(item):
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
        print(f"Error fetching flat {item['flat']}: {e}")
        return None


def uzb_flat_sale():
    # Step 1: Collect all flat links
    all_flat_links = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(get_flat_links, link) for link in page_links]
        for future in as_completed(futures):
            all_flat_links.extend(future.result())

    # Step 2: Fetch flat details concurrently
    results = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(scrape_flat_details, item) for item in all_flat_links]
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    return results
