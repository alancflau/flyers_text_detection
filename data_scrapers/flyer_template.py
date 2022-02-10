import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import clean_up

# For FoodBasics and Metro

class FlyerBot:
    def __init__(self,url):
        self.url = url
        self.current_path = os.getcwd()

        self.path = os.path.join(os.getcwd(), 'geckodriver.exe')
        service = Service(self.path)
        self.driver = webdriver.Firefox(service = service)
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.item_list = []
        self.price_list = []

    def bypass_login_postal_code(self,postal_code='M2N0C2'):

        iframe = self.driver.find_element(By.ID, "flipp-iframe")
        self.driver.switch_to.frame(iframe)
        # Step 1: Detect if it asks for postal code
        try:
            enter_post_code = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div[1]/form/div[1]/div/div[1]/div/input')))
            enter_post_code.send_keys(postal_code)
            enter_post_code.send_keys(Keys.ENTER)

            submit_click = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'submit_store_select')))
            submit_click.click()
        except:
            pass

    def choose_flyer(self):
        # Step 2: If asks to choose which flyer then
        try:
            flyer_click = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/div[2]/table/tbody/tr[1]/td[2]/a')))
            flyer_click.click()
        except:
            pass

    def find_Grid_View(self):
        grid_view = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='grid-view-label']")))
        grid_view.click()

    def collect_data(self):
        for item in self.driver.find_elements(By.CLASS_NAME, "item-name"):
            self.item_list.append(item.text)
        item_price = self.driver.find_elements(By.CLASS_NAME, "item-price")
        for price in item_price:
            label_price = price.get_attribute("aria-label")
            self.price_list.append(label_price)

    def close_driver(self):
        self.driver.close()

    def run(self):
        self.bypass_login_postal_code(postal_code='M2N0C2')
        self.choose_flyer()
        self.find_Grid_View()
        self.collect_data()
        df = clean_up(self.item_list, self.price_list)
        self.close_driver()
        return df




