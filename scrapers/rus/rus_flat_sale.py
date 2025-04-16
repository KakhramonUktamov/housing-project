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
    try:
        cleaned_text =re.sub(r"\s+", " ", text.replace("\xa0", " ").replace("\u202f", " ")).strip()
        return cleaned_text
    except Exception:
        return "N/A"



def rus_flat_sale(max_pages=5):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    results = []

    for page in range(1, max_pages + 1):
        url = f"https://www.avito.ru/all/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=&p={page}&s=104"

        for attempt in range(2):  # Try twice if needed
            try:
                driver.set_page_load_timeout(50)
                driver.get(url)
                break
            except Exception as e:
                if attempt == 1:
                    continue

        try:
            WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.CLASS_NAME, "iva-item-root-Se7z4"))
            )
        except Exception:
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.find_all("div", class_="iva-item-root-Se7z4")

        for card in cards:
            title_tag = card.find("div", class_="iva-item-title-CdRXl")
            price_tag = card.find("div", class_="price-priceContent-kPm_N")
            
            location_tag = card.find("div", class_="geo-root-NrkbV")
            date_tag = card.find("div", class_="iva-item-dateInfoStep-qcDJA")

            result = {
                "title": clean_text(title_tag.get_text()) if title_tag else "N/A",
                "price_info": clean_text(price_tag.get_text()) if price_tag else "N/A",
                "location": clean_text(location_tag.get_text()) if location_tag else "N/A",
                "date": clean_text(date_tag.get_text()) if date_tag else "N/A",
            }
            results.append(result)

        time.sleep(random.uniform(3, 6))

    driver.quit()
    print("✅ Scraping rus_flat_sale completed successfully.")
    print(f"Total listings scraped: {len(results)}")
    return results
