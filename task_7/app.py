import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT_FOLDER_PATH = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_FOLDER_PATH))
from utils.utils import SeleniumConnection
from task_7.bot import WorkUaBot


load_dotenv(Path(__file__).resolve().parent.joinpath('.env'))
debug_mode = os.environ['DEBUG_MODE']

WORKUA_URL = 'https://www.work.ua/'

if __name__ == '__main__':
    with SeleniumConnection(debug_mode) as driver:
        scrapper = WorkUaBot(driver)
        scrapper.driver.get(WORKUA_URL)
        scrapper.set_filters()
        scrapper.extract_urls()
        scrapper.extract_data()
        scrapper.save_data_csv()
