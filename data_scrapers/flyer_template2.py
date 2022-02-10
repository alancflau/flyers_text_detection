import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import clean_up

import pandas as pd

# For Longos, Loblaws

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
        self.product_lst = []
        self.price_value_lst = []
        self.save_amount_lst = []
        self.description_lst = []


    def flip_main_iframe(self):
        WebDriverWait(self.driver, 30).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@class='flippiframe productframe']")))

        # Don't use try and except
        try:
            postal_code = 'M2N0C2'
            location = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.ID, 'postal-input')))
            print('found it')
            location.send_keys(postal_code)
            location.send_keys(Keys.ENTER)

        except:
            pass

    def find_closest_store(self):
        # Click closest store
        try:
            time.sleep(2)
            button = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@class='select']")))
            # print(button)
            # print("found button")
            button.click()
        except:
            pass

    def find_main_content(self):
        self.driver.switch_to.default_content()
        time.sleep(5)
        WebDriverWait(self.driver, 30).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@class='flippiframe mainframe']")))

        # iframe = driver.find_element_by_xpath('//iframe[@class="flippiframe mainframe"]')
        # driver.switch_to.frame(iframe)
        # prdcts = self.driver.find_elements_by_xpath('//sfml-flyer-image//button')
        prdcts = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//sfml-flyer-image//button')))

        return prdcts

    def find_products(self, prdcts):
        j = 1
        counter_to_break = 0

        for i in prdcts:
            self.driver.execute_script("arguments[0].scrollIntoView();", i)
            i.click()

            time.sleep(3)

            i = 1
            while True:

                try:
                    button_link_to_text = '/html/body/flipp-router/flipp-publication-page/div/flipp-sfml-component/sfml-storefront/div/sfml-linear-layout/sfml-flyer-image[{}]/div/button[{}]'.format(
                        j, i)
                    button = self.driver.find_element_by_xpath(button_link_to_text)
                    self.driver.execute_script("arguments[0].click();", button)
                    # button.click()
                    # Switch to default content
                    self.driver.switch_to.default_content()
                    time.sleep(3)
                    # print(driver.page_source)
                    # iframe
                    WebDriverWait(self.driver, 30).until(
                        EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@class='flippiframe productframe']")))

                    # Product Name
                    try:
                        product_name = WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "primary-info-header")))
                        prod = product_name.text
                    except:
                        prod = ''
                    print(prod)
                    # Price Value
                    try:
                        price_value = WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "price-value")))
                        price = price_value.text
                    except:
                        price = ''

                    # Save amount
                    try:
                        save_amt = WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "salestory")))
                        saved = save_amt.text
                    except:
                        saved = ''

                    # description
                    try:
                        desc = WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "flipp-description")))
                        description = desc.text
                    except:
                        description = ''

                    self.product_lst.append(prod)
                    self.price_value_lst.append(price)
                    self.save_amount_lst.append(saved)
                    self.description_lst.append(description)

                    # print(button.get_attribute("aria-label"))
                    # switch back to other frmae

                    self.driver.switch_to.default_content()

                    # iframe = driver.find_element_by_xpath('//iframe[@class="flippiframe mainframe"]')

                    # self.driver.switch_to.frame(iframe)
                    WebDriverWait(self.driver, 30).until(
                        EC.frame_to_be_available_and_switch_to_it(
                            (By.XPATH, "//iframe[@class='flippiframe mainframe']")))

                    i += 1
                    counter_to_break = 0


                except:
                    counter_to_break += 1
                    break
            j += 1

            if counter_to_break >= 5:
                break
            print('----------------------')

    # Put this in utils.py later
    def collect_data(self):
        df = pd.DataFrame(list(zip(self.product_lst, self.price_value_lst, self.save_amount_lst, self.description_lst)),
                      columns=['Item', 'Price', 'Saved Amount', 'Description'])
        return df

    def close_driver(self):
        self.driver.close()

    def run(self):
        self.flip_main_iframe()
        self.find_closest_store()
        prdcts = self.find_main_content()
        self.find_products(prdcts)
        df = self.collect_data()
        self.close_driver()
        return df
