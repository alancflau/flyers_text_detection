import os
import time
import pandas as pd
import numpy as np


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
food_basics_flyer = "https://www.foodbasics.ca/flyer.en.html"

#Browser driver

options = FirefoxOptions()
options.add_argument("--headless")
path = r'C:\Users\alanc\Downloads\geckodriver-v0.30.0-win64\geckodriver.exe'
s = Service(path)
driver = webdriver.Firefox(service = s)
driver.maximize_window()
driver.get(food_basics_flyer)

#Put script to sleep for browser to load
time.sleep(3)

#postal code pop up
# postal_code = 'M2N0C2'
# enter_post_code = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/form/div[1]/div/div[1]/div/input')))
# enter_post_code.send_keys(postal_code)
# time.sleep(1)


iframe = driver.find_element(By.ID,"flipp-iframe")
driver.switch_to.frame(iframe)
# driver.switch_to.default_content()

#postal code pop up
postal_code = 'M2N0C2'
enter_post_code = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/form/div[1]/div/div[1]/div/input')))
enter_post_code.send_keys(postal_code)
enter_post_code.send_keys(Keys.ENTER)
time.sleep(1)

#REsume here
submit_click = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'submit_store_select')))
submit_click.click()
time.sleep(5)

flyer_click = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/table/tbody/tr[1]/td[2]/a')))
flyer_click.click()

time.sleep(5)
grid_view = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='grid-view-label']")))
# grid_view = driver.find_element_by_xpath("//div[@class='grid-view-label']")
grid_view.click()

#Collect data combine data into dictionary
item_list = []
price_list = []
for item in driver.find_elements(By.CLASS_NAME,"item-name"):
  item_list.append(item.text)
item_price = driver.find_elements(By.CLASS_NAME, "item-price")
for price in item_price:
  label_price = price.get_attribute("aria-label")
  price_list.append(label_price)

df = pd.DataFrame(list(zip(item_list, price_list)),
             columns =['Item','Price'])
df['Item'].replace('', np.nan, inplace=True)
df['Price'].replace('', np.nan, inplace=True)
df.dropna(subset=['Item','Price'], inplace=True)

print(df)
driver.close()