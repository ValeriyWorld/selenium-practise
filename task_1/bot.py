from time import sleep

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from utils.utils import BasicBot


class RozetkaBot(BasicBot):
    def smartphone_filter(self):
        producer_list = ['OnePlus', 'Samsung', 'Xiaomi']
        ram_list = ['12 ГБ', '8 ГБ']
        built_in_memory_list = ['128 ГБ', '256 ГБ']
        diagonal_list = ['6" - 6.49"', '6.5" и более']
        processor_list = ['Qualсomm Snapdragon', ]
        price_dict = {'min': '10000', 'max': '20000'}

        logger.debug('Choosing category for smartphones')
        self.find_click('//a[@class="menu-categories__link" and contains(text(),"Смартфоны")]').click()
        self.find_click(
            '//a[@class="tile-cats__heading tile-cats__heading_type_center ng-star-inserted" and '
            '@title="Мобильные телефоны"]'
        ).click()

        for filter_ in producer_list:
            logger.debug(f'Filter by producer: {filter_}')
            self.find_click(f'//div[@data-filter-name="producer"]//a[@data-id="{filter_}"]').click()
            sleep(1)

        for filter_ in ram_list:
            logger.debug(f'Filter by RAM: {filter_}')
            self.find_click(f'//div[@data-filter-name="38435"]//a[@data-id="{filter_}"]').click()
            sleep(1)

        for filter_ in built_in_memory_list:
            logger.debug(f'Filter by built-in memory: {filter_}')
            self.find_click(f'//div[@data-filter-name="41404"]//a[@data-id="{filter_}"]').click()
            sleep(1)

        for filter_ in diagonal_list:
            logger.debug(f'Filter by diagonal: {filter_}')
            self.find_click(f'//div[@data-filter-name="23777"]//a[@data-id=\'{filter_}\']').click()
            sleep(1)

        for filter_ in processor_list:
            logger.debug(f'Filter by processor: {filter_}')
            self.find_click(f'//div[@data-filter-name="protsessor-237281"]//a[@data-id="{filter_}"]').click()
            sleep(1)

        logger.debug('Filter by price: 10000 - 20000')
        for key, value in price_dict.items():
            price = self.find_click(f'//div[@data-filter-name="price"]//input[@formcontrolname="{key}"]')
            price.clear()
            price.send_keys(value)
        self.find_click('//div[@data-filter-name="price"]//button[@type="submit"]').click()

        logger.debug('Sorting smartphones by "Новинки"')
        Select(self.find_visibility('//div[@class="catalog-settings"]//select')).select_by_visible_text('Новинки')

        self.driver.execute_script('window.scrollTo(0, 0);')    # some browsers may need to scroll up in these place
        logger.debug('Select first 5 smartphones for comparison')
        sleep(1)
        first_five_phones = self.find_all_visibility(
            '//li[@class="catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted"]'
        )[0:5]
        for phone in first_five_phones:
            sleep(1)
            phone.find_element(By.XPATH, './/app-compare-button/button').click()

        logger.debug('Going to comparison page...')
        self.find_click('//button[@aria-label="Списки сравнения"]').click()
        self.find_click('//a[@class="comparison-modal__link"]').click()
        sleep(3)

        logger.debug('See for only differences')
        self.find_click('//button[contains(text(),"Только отличия")]').click()
