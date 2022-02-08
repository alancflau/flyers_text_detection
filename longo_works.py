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

url = 'https://www.longos.com/flyers'

options = FirefoxOptions()
# options.add_argument('--incognito')

path = r'C:\Users\alanc\Downloads\geckodriver-v0.30.0-win64\geckodriver.exe'
service = Service(path)
driver = webdriver.Firefox(service = service)
# driver.maximize_window()
driver.get(url)

WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@class='flippiframe productframe']")))

# Don't use try and except
try:
    postal_code = 'M2N0C2'
    location = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'postal-input')))
    print('found it')
    location.send_keys(postal_code)
    location.send_keys(Keys.ENTER)

except:
    pass

#Click closest store
try:
    time.sleep(2)
    button = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='select']")))
    print(button)
    print("found button")
    button.click()
except:
    pass

driver.switch_to.default_content()
time.sleep(5)

iframe = driver.find_element_by_xpath('//iframe[@class="flippiframe mainframe"]')
driver.switch_to.frame(iframe)
prdcts = driver.find_elements_by_xpath('//sfml-flyer-image//button')
print(len(prdcts)) #165
j = 1
counter_to_break = 0
for i in prdcts:
    driver.execute_script("arguments[0].scrollIntoView();", i)
    i.click()

    time.sleep(3)
    print(i)

    i = 1
    while True:

        try:
            button_link_to_text = '/html/body/flipp-router/flipp-publication-page/div/flipp-sfml-component/sfml-storefront/div/sfml-linear-layout/sfml-flyer-image[{}]/div/button[{}]'.format(j,i)
            button = driver.find_element_by_xpath(button_link_to_text)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(3)

            print(button.get_attribute("aria-label"))

            i+=1
            counter_to_break = 0

        except:
            counter_to_break+=1
            break
    j+=1

    if counter_to_break >=5:
        break
    print('----------------------')