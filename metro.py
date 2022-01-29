import os
import time
import pandas as pd
import numpy as np


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.common.keys import Keys
metro_flyer = "https://www.metro.ca/en/flyer"

#Browser driver

options = FirefoxOptions()
options.add_argument("--headless")
path = r'C:\Users\alanc\Downloads\geckodriver-v0.30.0-win64\geckodriver.exe'
s = Service(path)
driver = webdriver.Firefox(service = s)
driver.get(metro_flyer)

#Put script to sleep for browser to load
time.sleep(3)


# switch_iframe = driver.find_elements_by_tag_name("iframe")
switch_iframe = driver.find_elements(By.TAG_NAME, "iframe")
iframe = driver.find_element(By.ID,"flipp-iframe")
# iframe = driver.find_element_by_id("flipp-iframe")
driver.switch_to.frame(iframe)
grid_view = driver.find_element(By.XPATH,"//div[@class='grid-view-label']")
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