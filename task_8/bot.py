import os
from datetime import datetime
from time import sleep
from pathlib import Path

import pandas as pd
from loguru import logger
from selenium.webdriver.common.by import By

from utils.utils import BasicBot


class StocksBot(BasicBot):
    DATA_DIR_PATH = Path(__file__).resolve().parent.joinpath('data')
    DAYS_DELTA_UPDATE = 7

    def __init__(self, driver):
        super().__init__(driver)
        self.data_file_name = 'stock_tickers.csv'
        self.dataframe = None

    def get_data(self):
        data_last_updated = round(os.path.getmtime(self.DATA_DIR_PATH.joinpath(self.data_file_name)))
        now = round(datetime.timestamp(datetime.now()))
        update_delta = now - data_last_updated

        if update_delta > self.DAYS_DELTA_UPDATE * 24 * 60 * 60:
            columns = ['Symbol', 'Price']
            self.dataframe = pd.DataFrame(columns=columns)

            tickers = self.find_all_visibility('//div[contains(@class,"7")]//tbody/tr')
            for ticker in tickers:
                symbol = ticker.find_elements(By.XPATH, './td')[2].find_element(By.XPATH, './a').text.strip()
                price = ''.join(ticker.find_elements(By.XPATH, './td')[4].text.split(',')).strip()

                row_data = [symbol, price]
                self.dataframe = self.dataframe.append(dict(zip(columns, row_data)), ignore_index=True)
                logger.debug(f'Added! Symbol: {symbol}. Price: {price}')
            print(self.dataframe)
        else:
            logger.debug(f'STOCK TICKERS ARE UP TO DATE! Last update was {round(update_delta / 60 / 60)} hours ago.')

    def save_data_scv(self):
        if self.dataframe is not None:
            self.dataframe.to_csv(self.DATA_DIR_PATH.joinpath(self.data_file_name), index=False)
            logger.debug('Data has been successfully saved!')

    def compare_data(self):
        if self.dataframe is None:
            self.dataframe = pd.read_csv(self.DATA_DIR_PATH.joinpath(self.data_file_name))

        for i in self.dataframe.index:
            symbol = self.dataframe['Symbol'][i]
            price = self.dataframe['Price'][i]

            self.find_click('//input[@id="yfin-usr-qry"]').send_keys(symbol)
            sleep(1)
            self.find_click('//button[@id="header-desktop-search-button"]').click()
            sleep(5)
            try:
                np_xpath = '//fin-streamer[@data-field="postMarketPrice"]'
                new_price = float(''.join(self.find_presence(np_xpath).text.split(',')).strip())
                price_delta = new_price - price
                percentage_delta = round(abs(price_delta) * 100 / price, 3)
                if price_delta > 0 and percentage_delta > 1:
                    logger.info(f'SELL STOCKS!!! Symbol: {symbol}, price increased by {percentage_delta}%!!!')
                elif price_delta < 0 and percentage_delta > 1:
                    logger.info(f'BUY STOCKS!!! Symbol: {symbol}, price decreased by {percentage_delta}%!!!')
                else:
                    logger.debug(f'MINOR CHANGES!!! Symbol: {symbol}, price changed only by {percentage_delta}%.')
            except Exception:
                logger.debug(f'NO CURRENT PRICE INFO!!! Symbol: {symbol}, old price: {price}.')
