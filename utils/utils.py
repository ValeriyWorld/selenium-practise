from pathlib import Path
from platform import system
from time import time, sleep

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_driver(debug_mode, options):
    if debug_mode.lower() == 'true':
        driver_dir = Path(__file__).resolve().parents[1].joinpath('drivers')
        if system() == 'Windows':
            service = EdgeService(driver_dir.joinpath('msedgedriver_98_win32.exe'))
            init_driver = webdriver.Edge(service=service, options=options)
        elif system() == 'Linux':
            service = FirefoxService(driver_dir.joinpath('geckodriver_30_linux'))
            init_driver = webdriver.Firefox(service=service, options=options)
        else:
            raise Exception('Unsupported system! Possible: Windows, Linux')
    elif debug_mode.lower() == 'false':
        init_driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', options=options)
    else:
        raise Exception('Incorrect value was passed! Possible: True, true, False, false')
    return init_driver


class SeleniumConnection:
    def __init__(self, debug_mode, options=None, close=True):
        self.debug_mode = debug_mode
        self.options = options
        self.close = close
        self.driver = None
        self.scipt_time = None

    def __enter__(self):
        print('Selenium session started...')
        self.scipt_time = time()
        self.driver = get_driver(self.debug_mode, self.options)
        self.driver.maximize_window()
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.close:
            sleep(10)
            self.driver.quit()
        self.scipt_time = time() - self.scipt_time
        print(f'Selenium session stopped! Execution time = {self.scipt_time} seconds = {self.scipt_time/60} minutes.')


class BasicBot:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def find_visibility(self, xpath):
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def find_presence(self, xpath):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def find_click(self, xpath):
        return WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def find_all_visibility(self, xpath):
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))

    def find_all_presence(self, xpath):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
