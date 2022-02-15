import os
import time
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FlyerDynamicBot:
    def __init__(self,url):
        self.url = url
        self.current_path = os.getcwd()

        self.path = os.path.join(os.getcwd(), 'geckodriver.exe')
        service = Service(self.path)
        self.driver = webdriver.Firefox(service = service)
        self.driver.get(self.url)
        # self.driver.maximize_window()
        self.item_list = []
        self.price_list = []

        # Create lists
        self.info_lst = []

        self.wait_time = 10

    def find_location(self):
        try:
            addr = 'M2N0C2'
            location = WebDriverWait(self.driver, self.wait_time).until(
                EC.element_to_be_clickable((By.ID, 'location-search__search__input')))
            location.send_keys(addr)
            location.send_keys(Keys.ENTER)
        except:
            pass

    def find_flyer(self):
        try:
            flyer = WebDriverWait(self.driver, self.wait_time).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'flyers-location-search-item__main__content__button')))
            flyer.click()
        except:
            pass

        time.sleep(3)


    def find_iframe_and_switch(self):
        WebDriverWait(self.driver, self.wait_time).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@class="flippiframe mainframe"]')))

        # prdcts = WebDriverWait(self.driver, 30).until(
        #     EC.visibility_of_element_located((By.XPATH, '//sfml-flyer-image//a')))
        prdcts = self.driver.find_elements_by_xpath('//sfml-flyer-image//a')

        return prdcts

    def get_content(self,prdcts):
        j = 1
        counter_to_break = 0

        # Create lists
        # product_lst = []
        # price_value_lst = []
        # save_amount_lst = []
        # description_lst = []

        for i in prdcts:
            self.driver.execute_script("arguments[0].scrollIntoView();", i)

            print(i.get_attribute("aria-label"))
            self.info_lst.append(i.get_attribute("aria-label"))
            time.sleep(3)
            print(i)

    def collect_data(self):
        df = pd.DataFrame(self.info_lst,
                      columns=['Item'])
        return df

    def close_driver(self):
        self.driver.close()

    def run(self):
        self.find_location()
        self.find_flyer()
        prdcts = self.find_iframe_and_switch()
        self.get_content(prdcts)
        df = self.collect_data()
        self.close_driver()
        return df




