# -------- Documentation ----------
# python +3.11.0 install
# pip install selenium
# setup chrome.exe to system variable path in Development
# Download and place to C:\ driver,  https://googlechromelabs.github.io/chrome-for-testing/#stable 

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui
from time import sleep
from threading import Thread
from openpyxl import Workbook
import undetected_chromedriver as uc
import json, csv, random, os, sys

def Find_Element(driver : webdriver.Chrome, by, value : str) -> WebElement:
    while True:
        try:
            element = driver.find_element(by, value)
            break
        except:
            pass
        sleep(0.1)
    return element

def Find_Elements(driver : webdriver.Chrome, by, value : str) -> list[WebElement]:
    while True:
        try:
            elements = driver.find_elements(by, value)
            if len(elements) > 0:
                break
        except:
            pass
        sleep(0.1)
    return elements

def Send_Keys(element : WebElement, content : str):
    element.clear()
    for i in content:
        element.send_keys(i)
        sleep(0.1)
        
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get('https://www.cellphonerepair.com/stores-by-location')

# wait = WebDriverWait(driver, 50)
# element = wait.until(EC.presence_of_element_located((By.ID, 'cpr__state-select')))
# states = element.find_elements(By.TAG_NAME, "a")

states = driver.find_element(By.ID, 'cpr__state-select').find_elements(By.TAG_NAME, 'a')
print(f'***** Found {len(states)} States *****')
pre_states = []
for state in states:
    pre_state = state.get_attribute('href')
    pre_states.append(pre_state)
for state_url in pre_states:
    driver.get(state_url)
    cities = []
    cities = driver.find_elements(By.CLASS_NAME, 'website-link')
    print(f'----- Found {len(cities)} Cities -----')
    pre_cities = []
    for city in cities:
        pre_city = city.get_attribute('href')
        pre_cities.append(pre_city)
    for city_url in pre_cities:
        driver.get(city_url)
        try:
            facebook_url = driver.find_element(By.ID, 'widget-cpr-main-widgets-footer').find_element(By.CLASS_NAME, 'cpr__footer--certificate-sm').find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
            
            output = []
            output.append(city_url)
            output.append(facebook_url)
            print(output)
            
            open_out = open('output_url.csv','a',newline="", encoding='utf-8')
            file_o_csv = csv.writer(open_out, delimiter=',')
            file_o_csv.writerow(output)
            open_out.close()
        except:
            continue
print('-' * 10 + 'URLs Scraped' + '-' * 10)