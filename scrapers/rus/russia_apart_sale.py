from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import random

def clean_text(text):
        if not text:
            return "N/A"
        return re.sub(r"\s+", " ", text.replace("\xa0", " ").replace("\u202f", " ")).strip()


def scrape_avito(max_pages=5):

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)


    results = []

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}")
        url = f"https://www.avito.ru/all/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=&p={page}&s=104"

        driver.set_page_load_timeout(50)
    
        try:
            driver.get(url)
        except Exception as e:
            print(f"⚠️ Error loading {url}: {e}")
            continue
    
        try:
            WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.CLASS_NAME, "iva-item-root-Se7z4"))
            )
        except Exception as e:
            print(f"⚠️ Timeout on page {page}: {e}")
            continue
    
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.find_all("div", class_="iva-item-root-Se7z4")

        for card in cards:
            title_tag = card.find("div", class_="iva-item-title-CdRXl")
            price_tag = card.find("div", class_="price-priceContent-kPm_N")
            location_tag = card.find("div", class_="geo-root-NrkbV")
            seller_tag = card.find("span", class_="styles-module-noAccent-XIvJm styles-module-size_s-nEvE8")
            date_tag = card.find("div", class_="iva-item-dateInfoStep-qcDJA")

            result = {
            "title": clean_text(title_tag.get_text()) if title_tag else "N/A",
            "price": clean_text(price_tag.get_text()) if price_tag else "N/A",
            "location": clean_text(location_tag.get_text()) if location_tag else "N/A",
            "seller": clean_text(seller_tag.get_text()) if seller_tag else "N/A",
            "date": clean_text(date_tag.get_text()) if date_tag else "N/A",
            }


            results.append(result)
        time.sleep(random.uniform(3, 6))

    driver.quit()
    return results