from time import sleep
from pathlib import Path

from loguru import logger
import pandas as pd

from utils.utils import BasicBot


class OlxBot(BasicBot):
    def __init__(self, driver):
        super().__init__(driver)
        self.url_list = []
        self.dataframe = None

    def authenticate(self, cookies):
        logger.debug('Providing auth with cookies')
        for key, value in cookies.items():
            logger.debug(f'Set cookie: {key}')
            self.driver.add_cookie({"name": key, "value": value})

    def set_filters(self):
        status_list = ['new', ]
        diagonal_list = ['15"-15,6"', '16"-17"']
        brand_list = ['Apple', 'Acer', 'Asus', 'HP', 'Lenovo', 'LG', 'MSI', 'Samsung', 'Sony']
        price_dict = {'min': '10000', 'max': '100000'}

        logger.debug('Closing cookies pop-up...')
        self.find_click('//button[contains(@class,"cookie-close")]').click()
        sleep(3)

        logger.debug('Clicking on heading: "Електроніка"')
        self.find_click('//div[@class="item"]/a[@data-id="37"]').click()
        sleep(3)
        logger.debug('Clicking on sub-heading: "Ноутбуки та аксесуари"')
        self.find_click('//a[@data-id="1502"]').click()
        sleep(1)

        logger.debug('Selecting filter: "м. Львів, Львівська область"')
        for _ in range(2):
            self.find_click('//span[contains(text(),"Львів")]//parent::a[@class="link gray"]').click()
            sleep(3)

        logger.debug('Setting +10km')
        self.find_click('//a[@class="topLink"]').click()
        self.find_click('//a[text()="+ 10 km"]').click()
        sleep(1)

        logger.debug('Clicking on type "Вид товару"')
        self.find_visibility('//li[@id="param_subcat"]/div[contains(@class,"filter-item")]').click()
        logger.debug('Clicking on "Ноутбуки"')
        self.find_click('//a[@data-code="noutbuki"]').click()
        sleep(1)

        logger.debug('Clicking on "Стан"')
        self.find_click('//li[@data-key="state"]//a').click()
        logger.debug('Choosing statuses...')
        for filter_ in status_list:
            self.find_presence(f'//label[@data-value="{filter_}"]/span').click()
        sleep(1)

        logger.debug('Setting price range...')
        for key, value in price_dict.items():
            if key == 'min':
                self.find_presence('//span[@data-default-label="від"]').click()
            else:
                self.find_presence('//span[@data-default-label="до"]').click()
            self.find_presence(f'//li[@data-key="price"]//input[contains(@class,"{key}")]').send_keys(value)
        sleep(1)

        logger.debug('Clicking on "Діагональ екрану"')
        self.find_click('//li[@data-key="display_size"]//a').click()
        for filter_ in diagonal_list:
            logger.debug(f'Choosing diagonal: {filter_}')
            for_tag = self.find_presence(f'//input[@data-text=\'{filter_}\']').get_attribute('id')
            self.find_presence(f'//label[@for="{for_tag}"]/span').click()
        sleep(1)

        logger.debug('Clicking on "Марка ноутбуку"')
        self.find_click('//li[@data-key="laptop_manufacturer"]//a').click()
        for filter_ in brand_list:
            logger.debug(f'Choosing brand: {filter_}')
            for_tag = self.find_presence(f'//input[@data-text="{filter_}"]').get_attribute('id')
            self.find_presence(f'//label[@for="{for_tag}"]/span').click()
        sleep(3)

    def extract_urls(self):
        pagination_number = int(self.find_visibility('//a[@data-cy="page-link-last"]/span').text)
        logger.debug(f'Total number of pages: {pagination_number}')

        for page in range(1, pagination_number + 1):
            laptops = self.find_all_presence('//table[@id="offers_table"]//a[@data-cy]')
            logger.debug(f'Total number of urls on page #{page} - {len(laptops)}')
            for laptop in laptops:
                self.url_list.append(laptop.get_attribute('href'))
            if page != pagination_number:
                self.find_visibility('//a[@data-cy="page-link-next"]').click()
                sleep(3)
        logger.debug(f'Total urls added: {len(self.url_list)}')

    def extract_data(self):
        columns = ['Title', 'Advertisement ID', 'Brand', 'Diagonal', 'Price', 'Seller', 'Phone']
        self.dataframe = pd.DataFrame(columns=columns)

        urls = self.url_list
        for url_ in urls:
            logger.debug(f'Entering url {urls.index(url_)+1}: {url_}')
            self.driver.get(url_)
            sleep(3)

            title = self.find_presence('//h1[@data-cy="ad_title"]').text.strip()
            logger.info(f'Title: {title}')
            price = self.find_presence('//div[@data-testid="ad-price-container"]/h3').text.strip()
            logger.info(f'Price: {price}')
            brand = self.find_presence('//p[contains(text(),"Марка")]').text.split(':')[-1].strip()
            logger.info(f'Brand: {brand}')
            diagonal = self.find_presence('//p[contains(text(),"Діагональ")]').text.split(':')[-1].strip()
            logger.info(f'Diagonal: {diagonal}')
            id_ = self.find_presence('//span[contains(@class,"9xy3gn")]').text.split(':')[-1].strip()
            logger.info(f'Adv. ID: {id_}')
            seller = self.find_presence('//div[@data-cy="seller_card"]//h2').text.strip()
            logger.info(f'Seller: {seller}')

            phone_xpath = '//button[@data-cy="ad-contact-phone"]'
            try:
                self.find_click(phone_xpath).click()
                sleep(1)
                phone = ''.join(self.find_visibility(f'{phone_xpath}/span').text.strip().split())
            except Exception:
                phone = 'None'
            logger.info(f'Phone: {phone}')

            row_data = [title, id_, brand, diagonal, price, seller, phone]
            logger.debug(f'Advertisement added: {title}')
            self.dataframe = self.dataframe.append(dict(zip(columns, row_data)), ignore_index=True)
        print(self.dataframe)

    def save_data_csv(self):
        save_dir_path = Path(__file__).resolve().parent.joinpath('data')
        save_file_name = 'olx_laptops_adv.csv'
        self.dataframe.to_csv(save_dir_path.joinpath(save_file_name), index=False)
        logger.debug('Data has been successfully saved!')
