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

def ClickViewMore():
  viewMoreButton = driver.find_elements(By.CLASS_NAME, 'next')[-1]
  viewMoreButton.click()
  print('***** ViewMoreProducts Button Clicked *****')
  sleep(2)
  ClickViewMore()

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
item_num = 0

with open('urls.csv', 'r+', encoding='utf-8') as urls_file:
  urls = urls_file.readlines()
# wait = WebDriverWait(driver, 50)
# element = wait.until(EC.presence_of_element_located((By.ID, 'cpr__state-select')))
# states = element.find_elements(By.TAG_NAME, "a")

for brand_index, brand_url in enumerate(urls):
  driver.get(brand_url)
  print(f'~~~~~ {brand_index}th Brand: {brand_url.replace('\n', '')} ~~~~~')
  try:
    ClickViewMore()
  except:
    items = driver.find_elements(By.CLASS_NAME, 'product_addtocart_form')
    print(f'----- {len(items)} items found -----')
  items_url = []
  for item in items:
    item_url = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
    items_url.append(item_url)

  for item_url in items_url:
    item_price = ''
    item_partNum = ''
    item_model = ''
    
    driver.get(item_url)
    item_title = driver.find_element(By.CLASS_NAME, 'products-info-container').find_element(By.TAG_NAME, 'h1').text

    try:
      item_qty = driver.find_element(By.CLASS_NAME, 'products-info-container').find_element(By.CLASS_NAME, 'products-grade-attribute').text
      if 'QTY on hand:' in item_qty:
        item_qty = item_qty.split('QTY on hand:')[-1].strip()
      else:
        item_qty = ''
    except:
      item_qty = ''
    
    try:
      item_price = driver.find_element(By.CLASS_NAME, 'price-container').text.strip()
    except:
      item_price = ''
    
    item_descriptions = driver.find_element(By.CLASS_NAME, 'desc-section').text.split('\n\n')
    for item_description in item_descriptions:
      if 'Part Number' in item_description and ':' in item_description:
        item_partNum = item_description.split(':')[-1]
      elif 'Model Compat' in item_description and ':' in item_description:
        item_model = item_description.split(':')[-1].replace('\n', '')
      
    output = []
    item_num = item_num + 1
    print('-' * 3, item_num, '-' * 3)
    
    output.append(item_url)
    output.append(item_title)
    output.append('Replacement Laptop LCD LED Screen Display Monitor')
    output.append(item_price)
    output.append(item_partNum)
    output.append(item_model)
    output.append(item_qty)
    print(output)
    
    open_out = open('output_chromebookparts.csv','a',newline="", encoding='utf-8')
    file_o_csv = csv.writer(open_out, delimiter=',')
    file_o_csv.writerow(output)
    open_out.close()
    sleep(0.2)
print('~' * 5 + 'Finish' + '~' * 5)