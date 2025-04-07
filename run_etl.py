import json
import pandas as pd
from utils.logger import setup_logger

from scrapers.rus.russia_apart_sale import scrape_avito
from transformers.rus.russia_apart_sale_cleaner import clean_data
from loaders.rus.load_to_posgresql import database_loader

from scrapers.taj.taj_flat_sale import taj_flat_sale
from transformers.taj.taj_flat_sale_cleaner import taj_flat_sale_clean
from loaders.taj.load_taj_flat_sale import taj_flat_sale_loader

from scrapers.taj.taj_flat_rent import taj_flat_rent
from transformers.taj.taj_flat_rent_cleaner import taj_flat_rent_clean
from loaders.taj.load_taj_flat_rent import taj_flat_rent_loader

from scrapers.taj.taj_office_rent import taj_office_rent
from transformers.taj.taj_office_rent_cleaner import taj_office_rent_clean
from loaders.taj.load_taj_office_rent import taj_office_rent_loader

from scrapers.taj.taj_office_sale import taj_office_sale
from transformers.taj.taj_office_sale_cleaner import taj_office_sale_clean
from loaders.taj.load_taj_office_sale import taj_office_sale_loader

from scrapers.kaz.kaz_flat_sale import kaz_flat_sale
from transformers.kaz.kaz_flat_sale_cleaner import kaz_flat_sale_clean
from loaders.kaz.load_kaz_flat_sale import kaz_flat_sale_loader

from scrapers.kaz.kaz_flat_rent import kaz_flat_rent
from transformers.kaz.kaz_flat_rent_cleaner import kaz_flat_rent_clean
from loaders.kaz.load_kaz_flat_rent import kaz_flat_rent_loader

from scrapers.kaz.kaz_office_sale import kaz_office_sale
from transformers.kaz.kaz_office_sale_cleaner import kaz_office_sale_clean
from loaders.kaz.load_kaz_office_sale import kaz_office_sale_loader

from scrapers.kaz.kaz_office_rent import kaz_office_rent
from transformers.kaz.kaz_office_rent_cleaner import kaz_office_rent_clean
from loaders.kaz.load_kaz_office_rent import kaz_office_rent_loader

logger = setup_logger()
logger.info("Starting")

#Russian Apartment Sale
# def run_avito():
#     raw_data = scrape_avito(max_pages=3)
#     cleaned_data = clean_data(raw_data)
#     database_loader(cleaned_data)

# if __name__ == "__main__":
#     run_avito()


# #Tajikistan Apartment Sale
# def run_taj_flat_sale():
#     raw_data = taj_flat_sale()
#     clean_data=taj_flat_sale_clean(raw_data)
#     taj_flat_sale_loader(clean_data)

# if __name__ == "__main__":
#     run_taj_flat_sale()

# #Tajikistan Apartment Rent
# def run_taj_flat_rent():
#     raw_data = taj_flat_rent()
#     clean_data = taj_flat_rent_clean(raw_data)
#     taj_flat_rent_loader(clean_data)

# if __name__ == "__main__":
#     run_taj_flat_rent()

#Tajikistan Office Rent
# def run_taj_office_rent():
#     raw_data = taj_office_rent()
#     clean_data = taj_office_rent_clean(raw_data)
#     taj_office_rent_loader(clean_data)

# if __name__ == "__main__":
#     run_taj_office_rent()

#Tajikistan Office Sale
# def run_taj_office_sale():
#     raw_data = taj_office_sale()
#     clean_data = taj_office_sale_clean(raw_data)
#     taj_office_sale_loader(clean_data)

# if __name__ == "__main__":
#     run_taj_office_sale()

#Kazakhistan Flat Sale
# def run_kaz_flat_sale():
#     raw_data = kaz_flat_sale()
#     clean_data = kaz_flat_sale_clean(raw_data)
#     kaz_flat_sale_loader(clean_data)

# if __name__ == "__main__":
#     run_kaz_flat_sale()

#Kazakhistan Flat Rent
# def run_kaz_flat_rent():
#     raw_data = kaz_flat_rent()
#     clean_data = kaz_flat_rent_clean(raw_data)
#     kaz_flat_rent_loader(clean_data)

# if __name__ =="__main__":
#     run_kaz_flat_rent()

def run_kaz_office_sale():
    raw_data = kaz_office_sale()
    clean_data = kaz_office_sale_clean(raw_data)
    kaz_office_sale_loader(clean_data)

if __name__ =="__main__":
    run_kaz_office_sale()

#Kazakhistan Office Rent
# def run_kaz_office_rent():
#     raw_data = kaz_office_rent()
#     clean_data = kaz_office_rent_clean(raw_data)
#     kaz_office_rent_loader(clean_data)

# if __name__ == "__main__":
#     run_kaz_office_rent()

logger.info("Ending")