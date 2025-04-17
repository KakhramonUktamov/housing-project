from itertools import product
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

url_template = "https://www.olx.uz/nedvizhimost/kommercheskie-pomeshcheniya/prodazha/{location}/?currency=UYE&page={page}&search%5Bfilter_enum_premise_type%5D%5B0%5D=4&search%5Border%5D=created_at%3Adesc"

locations = ['tashkent', "toshkent-oblast", "andizhanskaya-oblast", "buharskaya-oblast", "dzhizakskaya-oblast",
             "karakalpakstan", "kashkadarinskaya-oblast", "navoijskaya-oblast", "namanganskaya-oblast",
             "samarkandskaya-oblast", "surhandarinskaya-oblast", "syrdarinskaya-oblast", "ferganskaya-oblast",
             "horezmskaya-oblast"]

pages = range(1, 26)

page_links = [
    url_template.format(location=loc, page=pg)
    for loc, pg in product(locations, pages)
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}


def fetch_office_sale_links(page_link):
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
        print(f"Error fetching page {page_link}: {e}")
        return []


def fetch_office_sale_details(item):
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
        print(f"Error fetching listing {item['flat']}: {e}")
        return None


def uzb_office_sale():
    flat_links = []
    # Step 1: Fetch all listing URLs
    with ThreadPoolExecutor(max_workers=20) as executor:
        for links in executor.map(fetch_office_sale_links, page_links):  # test with first 10
            flat_links.extend(links)

    results = []
    # Step 2: Fetch listing details
    with ThreadPoolExecutor(max_workers=20) as executor:
        for result in executor.map(fetch_office_sale_details, flat_links):
            if result:
                results.append(result)

    return results
