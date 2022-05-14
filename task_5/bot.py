import sys
from pathlib import Path

from loguru import logger

ROOT_FOLDER_PATH = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_FOLDER_PATH))
from task_4.utils import get_dom, rand_agent, rand_sleep


filters_tag = {
    'producer': 'producer',
    'ram': '38435',
    'built_in_memory': '41404',
    'diagonal': '23777',
    'processor': 'protsessor-237281',
    'price': 'price',
    'sort': 'sort'
}


class RozetkaBot:
    def __init__(self, url_, headers=None, cookies=None):
        self.url_ = url_
        self.headers = headers
        self.cookies = cookies
        self.filters = filters_tag

    def _get_smartphones_dom(self):
        page_dom = get_dom(self.url_, headers=rand_agent(self.headers))
        category_url = page_dom.xpath(
            '//a[@class="menu-categories__link" and contains(text(),"Смартфоны")]'
        )[0].get('href')
        logger.debug(f'Enter: {category_url}')
        rand_sleep(10, 15)

        category_dom = get_dom(category_url, headers=rand_agent(self.headers))
        smartphones_url = category_dom.xpath(
            '//a[@class="tile-cats__heading tile-cats__heading_type_center ng-star-inserted" and '
            '@title="Мобильные телефоны"]'
        )[0].get('href')
        logger.debug(f'Enter: {smartphones_url}')
        rand_sleep(10, 15)

        smartphones_dom = get_dom(smartphones_url, headers=rand_agent(self.headers))
        return smartphones_url, smartphones_dom

    def _get_filtered_dom(self):
        filters_dict = {
            'producer': ['OnePlus', 'Samsung', 'Xiaomi'],
            'ram': ['12 ГБ', '8 ГБ'],
            'built_in_memory': ['128 ГБ', '256 ГБ'],
            'diagonal': ['6" - 6.49"', '6.5" и более'],
            'processor': ['Qualсomm Snapdragon', ],
            'price': {'min': '10000', 'max': '20000'},
            'sort': 'novelty'
        }

        smartphones_url, smartphones_dom = self._get_smartphones_dom()
        filter_str_dict = {}
        for key, value in filters_dict.items():
            logger.debug(f'Filter by producer: {key}')
            if key == 'price':
                filter_str_dict[key] = value['min'] + '-' + value['max']
                continue
            if key == 'sort':
                filter_str_dict[key] = value
                continue

            filter_str = ''
            for filter_value in value:
                logger.debug(f'//div[@data-filter-name="{filters_tag[key]}"]//a[@data-id=\'{filter_value}\']')
                x = smartphones_dom.xpath(
                    f'//div[@data-filter-name="{filters_tag[key]}"]//a[@data-id=\'{filter_value}\']'
                )[0].get('href').split('/')[-2].split('=')[-1]
                filter_str = filter_str + x + ','
            filter_str = filter_str[:-1]
            filter_str_dict[key] = filter_str

        filtered_url = smartphones_url
        for fn in list(filters_tag.keys()):
            filtered_url = filtered_url + filters_tag[fn] + '=' + filter_str_dict[fn] + ';'
        filtered_url = filtered_url[:-1] + '/'
        logger.debug(f'Url with full filters: {filtered_url}')
        rand_sleep(10, 15)

        filtered_smartphones_dom = get_dom(filtered_url, headers=rand_agent(self.headers))
        return filtered_smartphones_dom

    def get_five_novelty(self):
        filtered_smartphones_dom = self._get_filtered_dom()

        smartphones_ids = [
            id_.get('data-goods-id')
            for id_ in filtered_smartphones_dom.xpath('//div[@data-goods-id]')[:5]
        ]
        comparison_url = f'https://rozetka.com.ua/comparison/c80003/ids={",".join(smartphones_ids)}/'
        logger.debug(f'Comparison url: {comparison_url}')
        rand_sleep(10, 15)

        comparison_dom = get_dom(comparison_url, headers=rand_agent(self.headers))
        smartphones_titles = [
            title.text
            for title in comparison_dom.xpath('//a[@class="product__heading"]')
        ]
        print(smartphones_titles)
