import requests
from datetime import datetime
import re
from bs4 import BeautifulSoup

from scrapers.uzb.uzb_flat_sale import uzb_flat_sale
from transformers.uzb.uzb_flat_sale_cleaner import uzb_flat_sale_clean
from loaders.uzb.load_uzb_flat_sale import uzb_flat_sale_loader

data = uzb_flat_sale()
cleaned_data = uzb_flat_sale_clean(data)
uzb_flat_sale_loader(cleaned_data)