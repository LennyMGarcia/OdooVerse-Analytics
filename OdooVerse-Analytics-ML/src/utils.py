import requests
import logging
import os
import sys

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger("odoo_logger")
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler(os.path.join(log_dir, 'error_log.log'))
file_handler.setLevel(logging.ERROR)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_error(error_message):
    try:
        logger.error(error_message)
        print(f"Error Message: {error_message}")
        sys.stdout.flush()
    except Exception as e:
        print(e)


def load_data(urls):
    responses = {}
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            responses[url] = response.json()
        else:
            print(f"Error getting data from {url}")
    
    return responses