import requests
from bs4 import BeautifulSoup

url = "https://tmcars.info/others/nedvijimost/prodaja-kvartir-i-domov?opts.emlakgornush=kwartira"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

cards = soup.find("span", class_="result-count").text
