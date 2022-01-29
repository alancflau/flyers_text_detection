import requests, itertools, re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
import time
import pandas as pd

walmart_flyer = "https://flyers.walmart.ca/flyers/accessibility/walmartcanada"

#Browser driver

options = FirefoxOptions()
options.add_argument("--headless")
path = r'C:\Users\alanc\Downloads\geckodriver-v0.30.0-win64\geckodriver.exe'
s = Service(path)
driver = webdriver.Firefox(service = s)
driver.maximize_window()
driver.get(walmart_flyer)

#Postal Code
postal_code = 'M2N0C2'

#Find and clear first
postal_enter = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'postal_code_text')))
postal_enter.clear()
postal_enter.send_keys(postal_code)
submit_click = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, ".//input[@value='Find Flyers' and @type='submit']")))
submit_click.click()
# postal_enter.send_keys(Keys.ENTER)
submit_click = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, ".//input[@value='Find Flyers' and @type='submit']")))
submit_click.click()
time.sleep(2)

src = driver.page_source
driver.close()
print(src)


soup = soup(src, 'html.parser')
innerContent = soup.find('h3')
# print(innerContent)

uls = []
for nextSibling in innerContent.findNextSiblings():
    if nextSibling.name == 'h2':
        break
    if nextSibling.name == 'ul':
        uls.append(nextSibling)

items = []
for ul in uls:
    for li in ul.findAll('li'):
        items.append(li.text)

print(items)

df = pd.DataFrame(items)
print(df)
