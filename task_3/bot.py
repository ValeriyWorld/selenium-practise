from time import sleep

from loguru import logger
from selenium.webdriver.common.by import By

from utils.utils import BasicBot


class FourPDABot(BasicBot):
    def __init__(self, driver):
        super().__init__(driver)
        self.topic_url_list = []

    def authenticate(self, cookies):
        logger.debug('Providing auth with cookies')
        for key, value in cookies.items():
            logger.debug(f'Set cookie: {key}')
            self.driver.add_cookie({"name": key, "value": value})

    def save_topics_url(self):
        logger.debug('Entering the "ФОРУМ"')
        self.find_click('//ul[@class="menu-main"]//a[contains(text(),"ФОРУМ")]').click()
        logger.debug('Entering the "Android - Программы" topic')
        self.find_click('//a[contains(@href,"showforum=212")]').click()
        logger.debug('Entering the "Программы для ПК" topic')
        self.find_click('//a[contains(@href,"showforum=558")]').click()

        logger.debug('Extracting the number of topic pages...')
        pages_number = int(self.find_presence('//span[@id="page-jump-1"]').text.split()[0])

        for page in range(1, pages_number + 1):
            logger.debug(f'Getting href over each topic on page: {page}')
            topics = self.find_all_presence('//a[contains(@id,"tid-link")]')
            for topic in topics:
                self.topic_url_list.append(topic.get_attribute('href'))
            sleep(0.5)
            if page != pages_number:
                logger.debug('Entering next page')
                next_page = self.find_all_presence('//a[@title="Следующая страница"]')[0]
                next_page.click()
        print(f'Amount of topics = {len(self.topic_url_list)}')

    def process_each_topic(self):
        urls = self.topic_url_list
        for url_ in urls:
            logger.debug(f'Entering url {urls.index(url_)+1}: {url_}')
            self.driver.get(url_)
            sleep(2)
            logger.debug('Going to the last page of current topic')
            last_page = self.driver.find_elements(By.XPATH, '//span[@class="pagelinklast"]')
            if last_page:
                last_page[0].click()

            logger.debug('Clicking on "Опции"')
            self.find_click('//div[@id="topicmenu-options"]/a').click()
            logger.debug('Clicking on "Добавить в избранное"')
            self.find_click('//div[@class="popupmenu-item"]/a[contains(text(),"Добавить в избранное")]').click()
            # logger.debug('Clicking on "Удалить из избранного"')
            # self.find_click('//div[@class="popupmenu-item"]/a[contains(text(),"Удалить из избранного")]').click()
            sleep(1)

            logger.debug('Clicking on "Опции"')
            self.find_click('//div[@id="topicmenu-options"]/a').click()
            logger.debug('Clicking on "Скачать тему"')
            self.find_click('//div[@class="popupmenu-item-last"]/a[contains(text(),"Скачать тему")]').click()
            logger.debug('Clicking on "HTML версия"')
            self.find_click('//a[contains(text(),"HTML версия")]').click()
            sleep(1)
        print('All topics have been successfully processed!')
