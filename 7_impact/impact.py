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
import json, random, os, csv

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

# service = Service(executable_path="C:\chromedriver-win64\chromedriver.exe")   
# options = Options()
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9000")
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url = 'https://www.impactcomputers.com/'
item_num = 0
process_log = []

driver.get(url)

def get_items(items):
  global item_num, log_indexes
  for index, item_url in enumerate(items):
    if log_indexes != [''] and log_indexes != []:
      index_value = int(log_indexes[0])
      if index < index_value:
        continue
      else:
        log_indexes.pop(0)
    elif os.path.isfile('E:\\Scraping\\usa_rahul\\work\\7_impact\\log.txt'):
      log_indexes = []
      log_in.close()
    print("Item URL:", item_url)
    driver.get(item_url)
    process_log.append(index)
    try:
      item_contents_link = []
      item_contents = driver.find_element(By.CLASS_NAME, 'content-box-1').find_elements(By.TAG_NAME, 'a')
      for item_content in item_contents:
        item_contents_link.append(item_content.get_attribute('href'))
      get_items(item_contents_link)
    except:
      print('=' * 20 + 'start' + '=' * 20)
      # save log info
      log_out = open('log.txt','w', encoding='utf-8')
      output_str = '-'.join(map(str, process_log))
      log_out.write(output_str)
      log_out.close()
      print(process_log)
      
      # identify page number
      try:
        page_nums = driver.find_element(By.CLASS_NAME, 'pagination').find_elements(By.CLASS_NAME, "page")
        page_num = page_nums[-3].text
      except:
        page_num = 1
      print("Page Number:", page_num)
      
      # start scraping
      for page_id in range(1, int(page_num) + 1):
        page_product_contents = []
        print(f'----- {page_id} Page')
        page_url = item_url + f'&page={page_id}'
        driver.get(page_url)
        page_contents = driver.find_elements(By.CLASS_NAME, 'product-module-item')
        for page_content in page_contents:
          page_item_title = page_content.find_element(By.TAG_NAME, 'h5').find_element(By.TAG_NAME, 'a').text.replace('  ', ' ')
          if 'motherboard' in page_item_title.lower() or 'circuit board' in page_item_title.lower() or 'battery' in page_item_title.lower() or 'keyboard' in page_item_title.lower() or 'desktop' in page_item_title.lower() or 'antenna' in page_item_title.lower() or 'wifi' in page_item_title.lower() or 'front cover' in page_item_title.lower() or 'back cover' in page_item_title.lower() or 'bottom base' in page_item_title.lower() or 'heatsink' in page_item_title.lower() or 'ac adapter' in page_item_title.lower() or 'ribbon' in page_item_title.lower():
            continue
          elif 'lcd' in page_item_title.lower() or 'led' in page_item_title.lower() or 'panel' in page_item_title.lower() or 'monitor' in page_item_title.lower() or 'display' in page_item_title.lower():
            page_product_contents.append(page_content.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        for page_item_url in page_product_contents:
            output = []
            item_num = item_num + 1
            print('-' * 10, item_num, '-' * 10)
            driver.get(page_item_url)
            
            # part number
            try:
              page_item_part = driver.find_element(By.CLASS_NAME, 'manufacturer-list').find_elements(By.TAG_NAME, 'li')[1].text.replace('Part Number:\n', '').strip()
            except:
              continue
              page_item_part = ''
              
            # price
            try:
              page_item_price = driver.find_element(By.CLASS_NAME, 'price-new').text.split(':')[1]
            except:
              page_item_price = ''
              
            output.append(page_item_url)
            output.append(page_item_title)
            output.append(page_item_part)
            output.append(page_item_price)
            output.append('Replacement Laptop LCD LED Screen Display')
            
            print(output)
            
            open_out = open('output.csv','a',newline="", encoding='utf-8')
            file_o_csv = csv.writer(open_out, delimiter=',')
            file_o_csv.writerow(output)
            open_out.close()
      print('-' * 20 + 'end' + '-' * 20)
    process_log.pop()

contents = driver.find_element(By.CLASS_NAME, 'panel-body').find_elements(By.TAG_NAME, 'a')
print(f'Brand Number: {len(contents)}')
if len(contents):
  for index, content in enumerate(contents):
    contents_link = []
    brand_url = content.get_attribute('href')
    print("*****Brand URL:", brand_url)
    
    # load log info
    if os.path.isfile('E:\\Scraping\\usa_rahul\\work\\7_impact\\log.txt'):
      with open('log.txt', 'r', encoding='utf-8') as log_in:
        if log_in:
          log_indexes = log_in.read().split('-')
        else:
          log_indexes = []
      if log_indexes != [''] and log_indexes != []:
        index_value = int(log_indexes[0])
        if index < index_value:
          continue
        elif index == index_value:
          log_indexes.pop(0)
        else:
          log_indexes = []
      else:
        log_in.close()
    else:
      log_indexes = []
    
    process_log.append(index)
    driver.get(brand_url)
    contents1 = driver.find_element(By.CLASS_NAME, 'content-box-1').find_elements(By.TAG_NAME, 'a')
    for content in contents1:
      contents_link.append(content.get_attribute('href'))
    print(f'Content Number: {len(contents_link)}')
    get_items(contents_link)
    process_log.pop()
    print('^' * 20 + 'NEXT BRAND' + '^' * 20)
  print('#' * 20 + 'Finish' + '#' * 20)