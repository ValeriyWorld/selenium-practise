from bot import RozetkaBot


ROZETKA_URL = 'https://rozetka.com.ua/ru/'
ROZETKA_HEADERS = {}


if __name__ == '__main__':
    scrapper = RozetkaBot(ROZETKA_URL, ROZETKA_HEADERS)
    scrapper.get_five_novelty()
