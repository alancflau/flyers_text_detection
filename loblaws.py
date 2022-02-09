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

url = 'https://www.loblaws.ca/print-flyer'

path = r'C:\Users\alanc\Downloads\geckodriver-v0.30.0-win64\geckodriver.exe'
s = Service(path)
driver = webdriver.Firefox(service = s)
# driver.maximize_window()
driver.get(url)

try:
    addr = 'M2N0C2'
    location = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, 'location-search__search__input')))
    location.send_keys(addr)
    location.send_keys(Keys.ENTER)
except:
    pass

# Choose flyer
try:
    flyer = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'flyers-location-search-item__main__content__button')))
    flyer.click()
except:
    pass

time.sleep(3)


iframe = driver.find_element_by_xpath('//iframe[@class="flippiframe mainframe"]')
driver.switch_to.frame(iframe)
prdcts = driver.find_elements_by_xpath('//sfml-flyer-image//a')
print(len(prdcts)) #165

j = 1
counter_to_break = 0

# Create lists
product_lst = []
price_value_lst = []
save_amount_lst = []
description_lst = []

for i in prdcts:
    driver.execute_script("arguments[0].scrollIntoView();", i)
    print(i.get_attribute("aria-label"))
    time.sleep(3)
    print(i)
