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


#Uzbekistan Flat Sale
def run_uzb_flat_sale():
    raw_data = uzb_flat_sale()
    clean_data = uzb_flat_sale_clean(raw_data)
    uzb_flat_sale_loader(clean_data)

if __name__ =="__main__":
    run_uzb_flat_sale()

# #Uzbekistan Flat Rent
# def run_uzb_flat_rent():
#     raw_data = uzb_flat_rent()
#     clean_data = uzb_flat_rent_clean(raw_data)
#     uzb_flat_rent_loader(clean_data)

# #Uzbekistan Office Sale
# def run_uzb_office_sale():
#     raw_data = uzb_office_sale()
#     clean_data = uzb_office_sale_clean(raw_data)
#     uzb_office_sale_loader(clean_data)

# #Uzbekistan Office Rent
# def run_uzb_office_rent():
#     raw_data = uzb_office_rent()
#     clean_data = uzb_office_rent_clean(raw_data)
#     uzb_office_rent_loader(clean_data)