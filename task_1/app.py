import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT_FOLDER_PATH = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_FOLDER_PATH))
from utils.utils import SeleniumConnection
from task_1.bot import RozetkaBot


load_dotenv(Path(__file__).resolve().parent.joinpath('.env'))
debug_mode = os.environ['DEBUG_MODE']

ROZETKA_URL = 'https://rozetka.com.ua/ru/'

if __name__ == '__main__':
    with SeleniumConnection(debug_mode) as driver:
        scrapper = RozetkaBot(driver)
        scrapper.driver.get(ROZETKA_URL)
        scrapper.smartphone_filter()
