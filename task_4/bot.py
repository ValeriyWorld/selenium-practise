from pathlib import Path

import pandas as pd
from loguru import logger

from utils import get_dom, rand_agent, rand_sleep, BasicScrapBot


class ComfyBot(BasicScrapBot):
    def extract_urls(self):
        comfy_smartphones_dom = get_dom(self.url_, headers=rand_agent(self.headers), cookies=self.cookies)
        logger.debug('Looking for last page in pagination...')
        pagination_number = int(comfy_smartphones_dom.xpath('//a[@class="pagination-item p-i"]/span')[-1].text)
        logger.debug(f'Total number of pages: {pagination_number}')

        for page in range(1, pagination_number + 1):
            rand_sleep(10, 15)
            logger.debug(f'Processing page #{page}...')
            url_ = self.url_ + f'?p={page}'
            dom = get_dom(url_, headers=rand_agent(self.headers), cookies=self.cookies)

            logger.debug('Extracting urls...')
            smartphones_xpath_list = dom.xpath('//a[@class="products-list-item__name"]')
            logger.debug(f'Total number of urls on this page: {len(smartphones_xpath_list)}')
            for smartphone in smartphones_xpath_list:
                self.url_list.append(smartphone.get('href'))
        # print(self.url_list)
        logger.debug(f'Total number of urls on all pages: {len(self.url_list)}')

    def extract_data(self):
        columns = ['Name', 'MPN', 'Price', 'Score', 'Availability']
        self.dataframe = pd.DataFrame(columns=columns)

        unprocessed_urls = []
        for url_ in self.url_list:
            rand_sleep(20, 25)
            smartphone_dom = get_dom(url_, headers=rand_agent(self.headers), cookies=self.cookies)

            name_xpath = smartphone_dom.xpath('//h1[@class="gen-tab__name"]/text()')
            if not name_xpath:
                unprocessed_urls.append(url_)
                # print(requests.get(url_, headers=rand_agent(self.headers), cookies=self.cookies).text)
                continue

            name = smartphone_dom.xpath('//h1[@class="gen-tab__name"]/text()')[0].strip()
            mpn = smartphone_dom.xpath('//span[@class="i-main__sku"]/text()')[0].strip().split()[-1]
            price = ''.join(
                smartphone_dom.xpath(
                    '//div[@class="price i-buy__price" or contains(@class,"out-of-stock")]'
                    '/div[@class="price__current"]/text()'
                )[0].strip().split()
            )
            score = smartphone_dom.xpath(
                '//div[@class="icon-comfy rating-box cursor-pointer"]'
                '/div[@class="icon-comfy rating-box__active"]/text()'
            )[0].strip()
            availability = smartphone_dom.xpath(
                '//button[@class="base-button row justify-center items-center no-wrap buy-btn i-buy__btn"]'
            )
            availability = 'InStock' if availability else 'OutOfStock'

            row_data = [name, mpn, price, score, availability]
            logger.debug(f'Phone added: {name}')
            self.dataframe = self.dataframe.append(dict(zip(columns, row_data)), ignore_index=True)
        print(f'Unprocessed urls:\n{unprocessed_urls}')
        print(f'Number of unprocessed urls: {len(unprocessed_urls)}')

    def save_data_csv(self):
        save_dir_path = Path(__file__).resolve().parent.joinpath('data')
        save_file_name = 'comfy_smartphones.csv'
        self.dataframe.to_csv(save_dir_path.joinpath(save_file_name), index=False)


# DOESN'T WORK PROPERLY.
# class EldoradoBot(BasicScrapBot):
#     def extract_urls(self):
#         rand_sleep(60, 80)
#         eldorado_laptops_dom = get_dom(self.url_, headers=rand_agent(self.headers), cookies=self.cookies)
#         logger.debug('Looking for last page in pagination...')
#         pagination_number = int(eldorado_laptops_dom.xpath('//a[@class="page-link"]')[-1].text)
#         logger.debug(f'Total number of pages: {pagination_number}')

#         for page in range(1, pagination_number + 1):
#             rand_sleep(60, 80)
#             logger.debug(f'Processing page #{page}...')
#             url_ = self.url_ + f'p={page}/'
#             dom = get_dom(url_, headers=rand_agent(self.headers), cookies=self.cookies)

#             logger.debug('Extracting urls...')
#             laptops_xpath_list = dom.xpath('//div[@class="title lp"]/a')
#             logger.debug(f'Total number of urls on this page: {len(laptops_xpath_list)}')
#             for laptop in laptops_xpath_list:
#                 self.url_list.append(laptop.get('href'))
#         print(self.url_list)
#         logger.debug(f'Total number of urls on all pages: {len(self.url_list)}')

#     def extract_data(self):
#         pass

#     def save_data_csv(self):
#         pass
