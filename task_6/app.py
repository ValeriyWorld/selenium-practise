import os
import sys
from time import sleep
from pathlib import Path

import schedule
from dotenv import load_dotenv

ROOT_FOLDER_PATH = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_FOLDER_PATH))
from utils.utils import SeleniumConnection
from task_6.bot import OlxBot


load_dotenv(Path(__file__).resolve().parent.joinpath('.env'))
debug_mode = os.environ['DEBUG_MODE']
credential_cookies = {
    'access_token': os.environ['ACCESS_TOKEN'],
    'refresh_token': os.environ['REFRESH_TOKEN'],
    'PHPSESSID': os.environ['PHPSESSID']
}

OLX_URL = 'https://www.olx.ua/uk/'


def scrapping_job():
    with SeleniumConnection(debug_mode) as driver:
        scrapper = OlxBot(driver)
        scrapper.driver.get(OLX_URL)
        scrapper.authenticate(credential_cookies)
        scrapper.set_filters()
        scrapper.extract_urls()
        scrapper.extract_data()
        scrapper.save_data_csv()


if __name__ == '__main__':
    schedule.every(50).minutes.do(scrapping_job)
    while True:
        schedule.run_pending()
        sleep(1)
