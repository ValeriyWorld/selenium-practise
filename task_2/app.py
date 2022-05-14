import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT_FOLDER_PATH = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_FOLDER_PATH))
from utils.utils import SeleniumConnection
from task_2.bot import FexNetBot


load_dotenv(Path(__file__).resolve().parent.joinpath('.env'))
debug_mode = os.environ['DEBUG_MODE']

FEXNET_URL = 'https://fex.net/en/'

if __name__ == '__main__':
    with SeleniumConnection(debug_mode) as driver:
        scrapper = FexNetBot(driver)
        scrapper.driver.get(FEXNET_URL)
        scrapper.automate_upload()
