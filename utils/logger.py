import logging
from datetime import datetime
from pathlib import Path

def setup_logger(name='etl_logger', log_dir='logs'):
    Path(log_dir).mkdir(exist_ok=True)
    log_file = f"{log_dir}/etl_{datetime.now().strftime('%Y_%m_%d')}.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
