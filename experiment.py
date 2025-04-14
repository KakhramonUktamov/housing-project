import requests
from bs4 import BeautifulSoup
import pandas as pd

# url = "https://www.house.kg/kupit-kvartiru?"
    
# results = []


# response = requests.get(url.format(1))
# soup = BeautifulSoup(response.content, "html.parser")

# page_max = int(soup.find_all("a", class_="page-link")[-1]['data-page'])


# cards = soup.find_all("div", class_="listing")


# for card in cards:

#     price = card.find("div", class_="price").get_text(strip=True)
#     title = card.find("p", class_="title").get_text(strip=True)
#     location = card.find("div", class_="address").get_text(strip=True)
#     date = card.find("div", class_="additional-info").get_text(strip=True)
   

#     result = {
#         "price": price,
#         "title": title,
#         "location": location,
#         "date": date
#     }
#     results.append(result)
 
# df = pd.DataFrame(results)



from scrapers.uzb.uzb_flat_sale import uzb_flat_sale
from transformers.uzb.uzb_flat_sale_cleaner import uzb_flat_sale_clean

raw_data = uzb_flat_sale()
df = uzb_flat_sale_clean(raw_data)


# response = requests.get("https://www.olx.uz/d/obyavlenie/3-xonali-uy-sotiladi-vokzalni-oldida-ID3YPRx.html")
# soup = BeautifulSoup(response.content, "html.parser")


