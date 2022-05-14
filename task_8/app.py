import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT_FOLDER_PATH = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_FOLDER_PATH))
from utils.utils import SeleniumConnection
from task_8.bot import StocksBot


load_dotenv(Path(__file__).resolve().parent.joinpath('.env'))
debug_mode = os.environ['DEBUG_MODE']

SLICKCHARTS_URL = 'https://www.slickcharts.com/sp500'
F_YAHOO_URL = 'https://finance.yahoo.com/'

if __name__ == '__main__':
    with SeleniumConnection(debug_mode, close=False) as driver:
        scrapper = StocksBot(driver)
        scrapper.driver.get(SLICKCHARTS_URL)
        scrapper.get_data()
        scrapper.save_data_scv()
        scrapper.driver.get(F_YAHOO_URL)
        scrapper.compare_data()
