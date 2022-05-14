from time import sleep
from pathlib import Path

import pandas as pd
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from utils.utils import BasicBot


class WorkUaBot(BasicBot):
    def __init__(self, driver):
        super().__init__(driver)
        self.url_list = []
        self.dataframe = None

    def js_clickable_click(self, xpath):
        return self.driver.execute_script('arguments[0].click();', self.find_click(xpath))

    def js_presence_click(self, xpath):
        return self.driver.execute_script('arguments[0].click();', self.find_presence(xpath))

    def set_filters(self):
        salary = {
            'min': {'text': '20000', 'value': '7'},
        }

        logger.debug('Clicking on "Вакансії за містами"')
        self.js_clickable_click('//li[@class="i-by-region"]/a')

        logger.debug('Clicking on "Львів"')
        self.js_clickable_click('//a[@id="lv"]')

        logger.debug('Clicking on "Розширений пошук"')
        self.js_clickable_click('//a[@id="adv-search"]')
        self.js_clickable_click('//a[@id="cat_more"]')

        logger.debug('Clicking on "IT, комп\'ютери, інтернет"')
        self.js_clickable_click('//div[contains(@class,"checkbox")]//a[contains(text(),"IT")]')
        sleep(1)

        logger.debug('Clicking on "Повна зайнятість"')
        self.js_clickable_click('//span[contains(text(),"Повна зайнятість")]/preceding-sibling::input')
        sleep(1)

        logger.debug(f'Setting min salary to {salary["min"]["text"]}')
        Select(self.find_visibility('//select[@id="salaryfrom_selection"]')).select_by_value(salary["min"]["value"])
        sleep(1)

        logger.debug('Filtering by "За зарплатою"')
        self.js_presence_click('//a[@data-sort="salary"]')
        sleep(1)

    def extract_urls(self):
        technologies = ['Python', 'Node.js', 'Java', 'C#', '.NET', 'React']

        pagination_xpath = '//ul[@class="pagination hidden-xs"]//a'
        pagination_number = int(self.find_all_visibility(pagination_xpath)[-2].text)
        logger.debug(f'Total number of pages: {pagination_number}')

        for page in range(1, pagination_number + 1):
            elements = self.find_all_presence('//div[contains(@class,"job-link")]')
            logger.debug(f'Total number of unfiltered advertisments on page #{page} - {len(elements)}')
            for element in elements:
                element_a = element.find_element(By.XPATH, './h2/a')
                element_title = element_a.text.strip()
                if any([t.lower() in element_title.lower() for t in technologies]):
                    logger.info(f'Filtered advertisment: {element_title}')
                    self.url_list.append(element_a.get_attribute('href'))
            if page < pagination_number:
                next_page = self.find_all_visibility(pagination_xpath)[-1]
                self.driver.execute_script('arguments[0].click();', next_page)
                sleep(3)
        logger.debug(f'Total urls added: {len(self.url_list)}')

    def extract_data(self):
        columns = [
            'Title', 'Salary', 'Employment info',
            'Company', 'Company address', 'Contact name', 'Contact phone'
        ]
        self.dataframe = pd.DataFrame(columns=columns)

        urls = self.url_list
        for url_ in urls:
            logger.debug(f'Entering url {urls.index(url_)+1}: {url_}')
            self.driver.get(url_)
            sleep(3)

            no_info = 'None'

            try:
                title = self.find_presence('//h1[@class="add-top-sm"]').text.strip()
            except Exception:
                title = no_info
            logger.info(f'Title: {title}')

            try:
                salary = self.find_presence('//span[@title="Зарплата"]/following-sibling::b').text.strip()
            except Exception:
                salary = no_info
            logger.info(f'Salary: {salary}')

            try:
                employment = self.find_presence('//span[@title="Умови й вимоги"]/..').text.strip()
            except Exception:
                employment = no_info
            logger.info(f'Employment info: {employment}')

            try:
                company = self.find_presence('//span[@title="Дані про компанію"]/../a').text.strip()
            except Exception:
                company = no_info
            logger.info(f'Company: {company}')

            try:
                company_address = self.find_presence('//span[@title="Адреса роботи"]/..').text.split('.')[0].strip()
            except Exception:
                company_address = no_info
            logger.info(f'Company address: {company_address}')

            try:
                contact_name = self.find_presence('//span[@title="Контакти"]/..').text.split('·')[0].strip()
            except Exception:
                contact_name = no_info
            logger.info(f'Contact: {contact_name}')

            phone_xpath = '//span[@id="contact-phone"]/a'
            try:
                self.js_clickable_click(phone_xpath)
                sleep(1)
                contact_phone = self.find_presence('//span[@id="contact-phone"]/a').text.strip()
            except Exception:
                contact_phone = no_info
            logger.info(f'Contact phone: {contact_phone}')

            row_data = [title, salary, employment, company, company_address, contact_name, contact_phone]
            logger.debug(f'Advertisement added: {title}')
            self.dataframe = self.dataframe.append(dict(zip(columns, row_data)), ignore_index=True)
        print(self.dataframe)

    def save_data_csv(self):
        save_dir_path = Path(__file__).resolve().parent.joinpath('data')
        save_file_name = 'workua_advertisements.csv'
        self.dataframe.to_csv(save_dir_path.joinpath(save_file_name), index=False)
        logger.debug('Data has been successfully saved!')
