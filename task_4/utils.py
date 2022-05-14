from abc import ABC, abstractmethod
from time import sleep

import requests
from random import uniform
from lxml.html import fromstring
from latest_user_agents import get_random_user_agent


def get_dom(url_, *args, **kwargs):
    page = requests.get(url_, *args, **kwargs)
    # page.encoding = 'utf-8'
    # print(page.text)
    dom_tree = fromstring(page.text)
    return dom_tree


def rand_agent(headers):
    return {**headers, 'User-Agent': get_random_user_agent()}


def rand_sleep(min_, max_):
    return sleep(round(uniform(min_, max_), 2))


class BasicScrapBot(ABC):
    def __init__(self, url_, headers=None, cookies=None):
        self.url_ = url_
        self.headers = headers
        self.cookies = cookies
        self.url_list = []
        self.dataframe = None

    @abstractmethod
    def extract_urls(self):
        pass

    @abstractmethod
    def extract_data(self):
        pass

    @abstractmethod
    def save_data_csv(self):
        pass
