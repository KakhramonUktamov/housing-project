import concurrent.futures
import time
import datetime
import traceback
from utils.logger import setup_logger

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%H%S")
log_filename = f"logs/etl_log_{timestamp}.log"
logger = setup_logger(log_filename)

from etl import run_rus_flat_sale
from etl import run_rus_flat_rent
from etl import run_rus_office_sale
from etl import run_rus_office_rent
from etl import run_taj_flat_sale
from etl import run_taj_flat_rent
from etl import run_taj_office_rent
from etl import run_taj_office_sale
from etl import run_kaz_flat_sale
from etl import run_kaz_flat_rent
from etl import run_kaz_office_sale
from etl import run_kaz_office_rent
from etl import run_kir_flat_sale
from etl import run_kir_flat_rent
from etl import run_kir_office_sale
from etl import run_kir_office_rent
from etl import run_uzb_flat_sale
from etl import run_uzb_flat_rent
from etl import run_uzb_office_sale
from etl import run_uzb_office_rent

def run_country_etl(country_name, funcs):

    print(f"🟦Starting ETL for {country_name}")
    logger.info(f"Starting ETL for {country_name}")
    country_start = time.time()

    for func in funcs:
        print(f"🟨Started:{func.__name__}")
        logger.info(f"Running: {func.__name__}")
        task_start = time.time()
        try:
            func()
            duration = time.time() - task_start
            print(f"✅Finished: {func.__name__} in {duration:.2f} seconds")
            logger.info(f"Completed: {func.__name__} in {duration:.2f} seconds")
        except Exception as e:
            print(f"🟥Failed: {func.__name__}")
            logger.error(f" Failed: {func.__name__}")
            logger.error(f"Error: {e}")
            logger.debug(traceback.format_exc())

    total = time.time() - country_start
    print(f"❗Finished ETL for {country_name} in {total:.2f} seconds")
    logger.info(f"Finished ETL for {country_name} in {total:.2f} seconds")


def main():
    start_time = time.time()

    country_etl_tasks = {

        "Tajikistan": [
            run_taj_flat_sale, run_taj_flat_rent, run_taj_office_rent, run_taj_office_sale
        ],
        # "Kazakhstan": [
        #      run_kaz_flat_sale, run_kaz_flat_rent, run_kaz_office_sale, run_kaz_office_rent
        #  ],
        # "Kyrgyzstan": [
        #     run_kir_flat_sale, run_kir_flat_rent, run_kir_office_sale, run_kir_office_rent
        # ],
        # "Uzbekistan": [
        #    run_uzb_flat_sale, run_uzb_flat_rent, run_uzb_office_sale, run_uzb_office_rent
        #  ],
        # "Russia": [
        #     run_rus_flat_sale, run_rus_flat_rent, run_rus_office_sale, run_rus_office_rent
        # ],
     }

    logger.info(" Starting parallel ETL execution by country")

    # === Run each country's ETL in parallel ===
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(run_country_etl, country, funcs)
            for country, funcs in country_etl_tasks.items()
        ]

        # Wait for all to complete
        concurrent.futures.wait(futures)

    total_duration = time.time() - start_time
    print(f"🚨All ETL completed in {total_duration:.2f} seconds")
    logger.info(f"All ETL completed in {total_duration:.2f} seconds")

if __name__ == "__main__":
    main()