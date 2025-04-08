import requests
from bs4 import BeautifulSoup

url = "https://www.house.kg/snyat-kommercheskaia-nedvijimost?commercial_type=2&region=all&sort_by=upped_at+desc?page={}"

def kir_office_rent():

    response_page = requests.get(url.format(1))
    page_soup = BeautifulSoup(response_page.content, "html.parser")
    page_max = int(page_soup.find_all("a", class_="page-link")[-1]['data-page'])
    
    results = []

    for page in range(1, 4):

        response = requests.get(url.format(page))
        soup = BeautifulSoup(response.content, "html.parser")

        cards = soup.find_all("div", class_="listing")

        for card in cards:

            price = card.find("div", class_="price").get_text(strip=True)
            title = card.find("p", class_="title").get_text(strip=True)
            location = card.find("div", class_="address").get_text(strip=True)
            date = card.find("div", class_="additional-info").get_text(strip=True)
            link = card.find("p", class_="title").find('a')['href']

            result = {
                "price": price,
                "title": title,
                "location_hs": location,
                "date": date,
                "link": "house.kg{}".format(link)
            }

            results.append(result)
    
    return results





