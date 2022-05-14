import os
from pathlib import Path

from dotenv import load_dotenv

from bot import ComfyBot  # , EldoradoBot


load_dotenv(Path(__file__).resolve().parent.joinpath('.env'))
COMFY_SMARTPHONES_URL = 'https://comfy.ua/smartfon/'
COMFY_HEADERS = {}
COMFY_COOKIES = {
    'active_city_id': os.environ['COMFY_ACTIVE_CITY_ID'],
    'incap_ses_1524_1858972': os.environ['COMFY_INCAP_SES_1524_1858972'],
    'incap_ses_324_1858972': os.environ['COMFY_INCAP_SES_324_1858972'],
    'incap_ses_770_1858972': os.environ['COMFY_INCAP_SES_770_1858972'],
    'incap_sh_1858972': os.environ['COMFY_INCAP_SH_1858972'],
    'language': os.environ['COMFY_LANGUAGE'],
    'nlbi_1858972': os.environ['COMFY_NLBI_1858972'],
    'nlbi_1858972_2147483646': os.environ['COMFY_NLBI_1858972_2147483646'],
    'rcuid': os.environ['COMFY_RCUID']
}
# ELDORADO_SMARTPHONES_URL = 'https://eldorado.ua/uk/notebooks/c1039096/'
# ELDORADO_HEADERS = {}
# ELDORADO_COOKIES = {
#     'userGUID': os.environ['ELDORADO_USER_GUID'],
#     'ModalLeftProductsStatus': os.environ['ELDORADO_MODAL_LEFT_PRODUCTS_STATUS'],
#     'incap_ses_800_1842303': os.environ['ELDORADO_INCAP_SES_800_1842303'],
#     'incap_ses_767_1842303': os.environ['ELDORADO_INCAP_SES_767_1842303'],
#     'incap_ses_325_1842303': os.environ['ELDORADO_INCAP_SES_325_1842303'],
#     'incap_ses_1288_1842303': os.environ['ELDORADO_INCAP_SES_1288_1842303'],
#     'incap_ses_521_1842303': os.environ['ELDORADO_INCAP_SES_521_1842303']
# }

if __name__ == '__main__':
    scrapper = ComfyBot(COMFY_SMARTPHONES_URL, COMFY_HEADERS, COMFY_COOKIES)
    scrapper.extract_urls()
    scrapper.extract_data()
    scrapper.save_data_csv()

    # scrapper = EldoradoBot(ELDORADO_SMARTPHONES_URL, ELDORADO_HEADERS, ELDORADO_COOKIES)
    # scrapper.extract_urls()
    # scrapper.extract_data()
    # scrapper.save_data_csv()
