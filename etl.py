
from scrapers.rus.rus_flat_sale import rus_flat_sale
from transformers.rus.rus_flat_sale_cleaner import rus_flat_sale_clean
from loaders.rus.load_rus_flat_sale import rus_flat_sale_loader

from scrapers.rus.rus_flat_rent import rus_flat_rent
from transformers.rus.rus_flat_rent_cleaner import rus_flat_rent_clean
from loaders.rus.load_rus_flat_rent import rus_flat_rent_loader

from scrapers.rus.rus_office_sale import rus_office_sale
from transformers.rus.rus_office_sale_cleaner import rus_office_sale_clean
from loaders.rus.load_rus_office_sale import rus_office_sale_loader

from scrapers.rus.rus_office_rent import rus_office_rent
from transformers.rus.rus_office_rent_cleaner import rus_office_rent_clean
from loaders.rus.load_rus_office_rent import rus_office_rent_loader

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

from scrapers.kir.kir_flat_sale import kir_flat_sale
from transformers.kir.kir_flat_sale_cleaner import kir_flat_sale_clean
from loaders.kir.load_kir_flat_sale import kir_flat_sale_loader

from scrapers.kir.kir_flat_rent import kir_flat_rent
from transformers.kir.kir_flat_rent_cleaner import kir_flat_rent_clean
from loaders.kir.load_kir_flat_rent import kir_flat_rent_loader

from scrapers.kir.kir_office_sale import kir_office_sale
from transformers.kir.kir_office_sale_cleaner import kir_office_sale_clean
from loaders.kir.load_kir_office_sale import kir_office_sale_loader

from scrapers.kir.kir_office_rent import kir_office_rent
from transformers.kir.kir_office_rent_cleaner import kir_office_rent_clean
from loaders.kir.load_kir_office_rent import kir_office_rent_loader

from scrapers.uzb.uzb_flat_sale import uzb_flat_sale
from transformers.uzb.uzb_flat_sale_cleaner import uzb_flat_sale_clean
from loaders.uzb.load_uzb_flat_sale import uzb_flat_sale_loader

from scrapers.uzb.uzb_flat_rent import uzb_flat_rent
from transformers.uzb.uzb_flat_rent_cleaner import uzb_flat_rent_clean
from loaders.uzb.load_uzb_flat_rent import uzb_flat_rent_loader

from scrapers.uzb.uzb_office_sale import uzb_office_sale
from transformers.uzb.uzb_office_sale_cleaner import uzb_office_sale_clean
from loaders.uzb.load_uzb_office_sale import uzb_office_sale_loader

from scrapers.uzb.uzb_office_rent import uzb_office_rent
from transformers.uzb.uzb_office_rent_cleaner import uzb_office_rent_clean
from loaders.uzb.load_uzb_office_rent import uzb_office_rent_loader

#Russian Apartment Sale
def run_rus_flat_sale():
    raw_data = rus_flat_sale()
    cleaned_data = rus_flat_sale_clean(raw_data)
    rus_flat_sale_loader(cleaned_data)

#Russian Flat Rent
def run_rus_flat_rent():
    raw_data = rus_flat_rent()
    clean_data = rus_flat_rent_clean(raw_data)
    rus_flat_rent_loader(clean_data)

#Russian Office Sale
def run_rus_office_sale():
    raw_data = rus_office_sale()
    clean_data = rus_office_sale_clean(raw_data)
    rus_office_sale_loader(clean_data)

#Russian Office Rent
def run_rus_office_rent():
    raw_data = rus_office_rent()
    clean_data = rus_office_rent_clean(raw_data)
    rus_office_rent_loader(clean_data)

#Tajikistan Apartment Sale
def run_taj_flat_sale():
    raw_data = taj_flat_sale()
    clean_data=taj_flat_sale_clean(raw_data)
    taj_flat_sale_loader(clean_data)

#Tajikistan Apartment Rent
def run_taj_flat_rent():
    raw_data = taj_flat_rent()
    clean_data = taj_flat_rent_clean(raw_data)
    taj_flat_rent_loader(clean_data)

#Tajikistan Office Rent
def run_taj_office_rent():
    raw_data = taj_office_rent()
    clean_data = taj_office_rent_clean(raw_data)
    taj_office_rent_loader(clean_data)

#Tajikistan Office Sale
def run_taj_office_sale():
    raw_data = taj_office_sale()
    clean_data = taj_office_sale_clean(raw_data)
    taj_office_sale_loader(clean_data)

#Kazakhistan Flat Sale
def run_kaz_flat_sale():
    raw_data = kaz_flat_sale()
    clean_data = kaz_flat_sale_clean(raw_data)
    kaz_flat_sale_loader(clean_data)

#Kazakhistan Flat Rent
def run_kaz_flat_rent():
    raw_data = kaz_flat_rent()
    clean_data = kaz_flat_rent_clean(raw_data)
    kaz_flat_rent_loader(clean_data)

#Kazakhistan Office Sale
def run_kaz_office_sale():
    raw_data = kaz_office_sale()
    clean_data = kaz_office_sale_clean(raw_data)
    kaz_office_sale_loader(clean_data)

#Kazakhistan Office Rent
def run_kaz_office_rent():
    raw_data = kaz_office_rent()
    clean_data = kaz_office_rent_clean(raw_data)
    kaz_office_rent_loader(clean_data)

#Kirgizistan Flat Sale
def run_kir_flat_sale():
    raw_data = kir_flat_sale()
    clean_data = kir_flat_sale_clean(raw_data)
    kir_flat_sale_loader(clean_data)

#Kirgizistan Flat Rent
def run_kir_flat_rent():
    raw_data = kir_flat_rent()
    clean_data = kir_flat_rent_clean(raw_data)
    kir_flat_rent_loader(clean_data)

#Kirgizistan Office Sale
def run_kir_office_sale():
    raw_data = kir_office_sale()
    clean_data = kir_office_sale_clean(raw_data)
    kir_office_sale_loader(clean_data)

#Kirgizistan Office Rent
def run_kir_office_rent():
    raw_data = kir_office_rent()
    clean_data = kir_office_rent_clean(raw_data)
    kir_office_rent_loader(clean_data)

#Uzbekistan Flat Sale
def run_uzb_flat_sale():
    raw_data = uzb_flat_sale()
    clean_data = uzb_flat_sale_clean(raw_data)
    uzb_flat_sale_loader(clean_data)

#Uzbekistan Flat Rent
def run_uzb_flat_rent():
    raw_data = uzb_flat_rent()
    clean_data = uzb_flat_rent_clean(raw_data)
    uzb_flat_rent_loader(clean_data)

#Uzbekistan Office Sale
def run_uzb_office_sale():
    raw_data = uzb_office_sale()
    clean_data = uzb_office_sale_clean(raw_data)
    uzb_office_sale_loader(clean_data)

#Uzbekistan Office Rent
def run_uzb_office_rent():
    raw_data = uzb_office_rent()
    clean_data = uzb_office_rent_clean(raw_data)
    uzb_office_rent_loader(clean_data)