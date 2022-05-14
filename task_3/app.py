import os
import sys
from pathlib import Path
from platform import system

from dotenv import load_dotenv
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

ROOT_FOLDER_PATH = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_FOLDER_PATH))
from utils.utils import SeleniumConnection
from task_3.bot import FourPDABot


download_dir_path = Path(__file__).resolve().parent.joinpath('Downloaded_topics')
if system() == 'Windows':
    options = EdgeOptions()
    options.add_experimental_option(
        'prefs', {
            'download.default_directory': str(download_dir_path),
            'download.directory_upgrade': True,
            'download.prompt_for_download': False,
            'safebrowsing.enabled': False,
            'safebrowsing.disable_download_protection': True,
            'plugins.always_open_pdf_externally': True,      # disables PDF viewer plugins - prevents from opening in browser
            'profile.default_content_settings.popups': '0',
            'profile.content_settings.exceptions.automatic_downloads.*.setting': '1',
            'args': [
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ],
            'useAutomationExtension': 'false'
        }
    )
elif system() == 'Linux':
    options = FirefoxOptions()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference(
        "browser.download.dir",
        str(download_dir_path)
    )
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/html; charset=windows-1251")
else:
    raise Exception('Unsupported system! Possible: Windows, Linux')

load_dotenv(Path(__file__).resolve().parent.joinpath('.env'))
debug_mode = os.environ['DEBUG_MODE']
credential_cookies = {
    'member_id': os.environ['FPDA_MEMBER_ID'],
    'pass_hash': os.environ['FPDA_PASS_HASH']
}

FOURPDA_URL = 'https://4pda.to/'

if __name__ == '__main__':
    with SeleniumConnection(debug_mode, options=options) as driver:
        scrapper = FourPDABot(driver)
        scrapper.driver.get(FOURPDA_URL)
        scrapper.authenticate(credential_cookies)
        scrapper.save_topics_url()
        scrapper.process_each_topic()
