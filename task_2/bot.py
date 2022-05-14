from time import sleep
from pathlib import Path

from loguru import logger
from selenium.webdriver.common.by import By

from utils.utils import BasicBot


class FexNetBot(BasicBot):
    def automate_upload(self):
        upload_dir_path = Path(__file__).resolve().parent.joinpath('fake_upload')
        files_to_upload = ['file1.txt', 'file2.txt', 'file3.txt']
        create_folder_name = 'Folder'

        sleep(5)
        self.find_presence('//div[contains(@id,"epom-close-wrapper")]/div[contains(@class,"close")]').click()
        logger.debug('Clicking on Send Files')
        self.find_click('//div[@class="flex flex_justify_center margin_bottom_100"]/button').click()
        logger.debug('Uploading files...')

        for file in files_to_upload:
            logger.debug('Clicking on Upload')
            self.find_click(
                '//button[@class="button button_theme_primary button_size_normal button_type_dir-menu"]'
            ).click()
            sleep(2)
            logger.debug(f'Upload file: {file}')
            uploader = self.find_presence('//ul//input[@type="file" and @multiple]')
            sleep(2)
            uploader.send_keys(str(upload_dir_path.joinpath(file)))
            if files_to_upload.index(file) == 0:
                sleep(15)
            self.find_click('//span[@class="modal__close-btn"]').click()

        logger.debug('Creating folder...')
        self.find_click(
            '//button[@class="button button_theme_secondary button_size_normal button_type_dir-menu"]'
        ).click()
        logger.debug('Entering folder name')
        self.find_visibility('//input[@type="text" and @name="name"]').send_keys(create_folder_name)
        logger.debug('Submit folder name')
        self.find_click('//footer[@class="modal__footer border"]//button[contains(@class,"primary")]').click()
        sleep(1)

        logger.debug('Selecting All files')
        self.find_presence('//div[@class="container container_width_primary"]//input[@type="checkbox"]').click()
        logger.debug('Unselecting folder')
        self.find_presence('//div[contains(@class,"type_dir")]//input[@type="checkbox"]').click()
        logger.debug('Click Move button')
        self.find_presence('//li[@class="table-manage-menu__item"]//span[contains(text(),"Move")]').click()
        logger.debug('Moving to Folder')
        self.find_visibility(
            f'//li[@class="tree-manage-list__item"]//span[contains(text(),"{create_folder_name}")]'
        ).click()
        self.find_visibility('//footer[@class="modal__footer"]//button[contains(@class,"primary")]').click()
        sleep(1)
        logger.debug('Go to the Folder')
        self.find_visibility(
            f'//div[contains(@class,"type_dir")]//div[contains(text(),"{create_folder_name}")]'
        ).click()

        item_xpath = '//div[@class="fs-table__row"]'
        item_name_xpath = './/span[@class="text_overflow_ellipsis"]'
        sleep(2)
        for f in self.find_all_visibility(item_xpath):
            if f.find_element(By.XPATH, item_name_xpath).text == 'file2':
                logger.debug('Delete file2.txt')
                f.find_element(By.XPATH, './/input[@type="checkbox"]').click()
                self.find_visibility('//li[@class="table-manage-menu__item"]//span[contains(text(),"Delete")]').click()
                self.find_click(
                    '//footer[contains(@class,"modal__footer")]//button[contains(@class,"primary")]'
                ).click()
                break

        sleep(2)
        for f in self.find_all_visibility(item_xpath):
            if f.find_element(By.XPATH, item_name_xpath).text == 'file1':
                logger.debug('Rename file1.txt to file1_new.txt')
                f.find_element(
                    By.XPATH,
                    './/div[@class="tooltip-anchor node-controls__item node-controls__item_type_more"]//button'
                ).click()
                self.find_click('//div[contains(@class,"rename")]/button').click()
                self.find_visibility('//input[@data-qa="renameNodeForm_name"]').send_keys('_new')
                self.find_click(
                    '//footer[contains(@class,"modal__footer")]//button[contains(@class,"primary")]'
                ).click()
                break

        sleep(1)
        logger.debug('Go back in browser')
        self.driver.execute_script("window.history.go(-1)")

        logger.debug('Clicking on Upload')
        self.find_click(
            '//button[@class="button button_theme_primary button_size_normal button_type_dir-menu"]'
        ).click()
        sleep(2)
        logger.debug('Upload file: file3.txt')
        uploader = self.find_presence('//ul//input[@type="file" and @multiple]')
        sleep(2)
        uploader.send_keys(str(upload_dir_path.joinpath('file3.txt')))
        self.find_click('//span[@class="modal__close-btn"]').click()
