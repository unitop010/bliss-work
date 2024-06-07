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
from datetime import datetime
from time import sleep
import json, csv, random, os, sys

# Set options for WebDriver to run in headless mode
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')  # This option may be unnecessary in some cases
# options.add_experimental_option('excludeSwitches', ['enable-logging'])  # To suppress logging messages
# driver = webdriver.Chrome(options=options)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url = 'https://www.impactcomputers.com/'
item_num = 0
process_log = []

with open('keywords.csv', 'r+', encoding='utf-8') as keywords:
  all_keywords = keywords.readlines()
  all_keywords.reverse()

def get_items(items):
  global item_num, log_indexes
  for index, item_url in enumerate(items):
    if log_indexes != [''] and log_indexes != []:
      index_value = int(log_indexes[0])
      if index < index_value:
        continue
      else:
        log_indexes.pop(0)
    elif os.path.isfile('C:\\Users\\rahul\\Documents\\Work\\7_impact\\2.0\\log.txt'):
      log_indexes = []
      log_in.close()
    print("Item URL:", item_url)
    driver.get(item_url)
    process_log.append(index)
    try:
      item_contents = [link.get_attribute('href') for link in driver.find_element(By.CLASS_NAME, 'content-box-1').find_elements(By.TAG_NAME, 'a')]
      get_items(item_contents)
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
        page_num = driver.find_element(By.CLASS_NAME, 'pagination').find_elements(By.CLASS_NAME, "page")
        page_num = page_num[-3].text
      except:
        page_num = 1
      print("Page Number:", page_num)
      
      # start scraping
      for page_id in range(1, int(page_num) + 1):
        print(f'----- {page_id} Page')
        page_url = item_url + f'&page={page_id}'
        driver.get(page_url)
        page_item_urls = []
        page_contents = driver.find_elements(By.CLASS_NAME, 'product-module-item')
        for page_content in page_contents:
          page_product_title = page_content.find_element(By.TAG_NAME, 'h5').find_element(By.TAG_NAME, 'a').text.replace('  ', ' ')
          page_product_title_raw = ''.join(page_product_title.split(' - ')[1:])
          if 'board' in page_product_title_raw.lower() or 'circuit board' in page_product_title_raw.lower() or 'battery' in page_product_title_raw.lower() or 'keyboard' in page_product_title_raw.lower() or 'desktop' in page_product_title_raw.lower() or 'antenna' in page_product_title_raw.lower() or 'wifi' in page_product_title_raw.lower() or 'front cover' in page_product_title_raw.lower() or 'back cover' in page_product_title_raw.lower() or 'bottom base' in page_product_title_raw.lower() or 'heatsink' in page_product_title_raw.lower() or 'ac adapter' in page_product_title_raw.lower() or 'ribbon' in page_product_title_raw.lower() or 'cable' in page_product_title_raw.lower() or 'bezel' in page_product_title_raw.lower() or 'hinge' in page_product_title_raw.lower() or 'cover' in page_product_title_raw.lower() or 'screw' in page_product_title_raw.lower():
            continue
          elif 'lcd' in page_product_title_raw.lower() or 'led' in page_product_title_raw.lower() or 'panel' in page_product_title_raw.lower() or 'monitor' in page_product_title_raw.lower() or 'display' in page_product_title_raw.lower():
            for keyword_index, keyword in enumerate(all_keywords):
              size = keyword.replace('\n', '')
              if size in page_product_title_raw.lower():
                page_item_urls.append(page_content.find_element(By.TAG_NAME, 'h5').find_element(By.TAG_NAME, 'a').get_attribute('href'))
                break
              else:
                continue
          else:
            continue
        for page_item_url in page_item_urls:
          driver.get(page_item_url)

          output = []
          # title
          try:
            page_item_title = driver.find_element(By.CLASS_NAME, 'page-heading-2').text.strip()
          except:
            page_item_title = ''
            
          # part number
          try:
            page_item_part = driver.find_element(By.CLASS_NAME, 'manufacturer-list').find_elements(By.TAG_NAME, 'li')[1].text.replace('Part Number:', '').strip()
          except:
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
          output.append('Replacement Laptop LCD LED Screen Display Monitor')
          
          item_num = item_num + 1
          print('-' * 10, item_num, '-' * 10)
          print(output)
          
          open_out = open('output_impact.csv','a',newline="", encoding='utf-8')
          file_o_csv = csv.writer(open_out, delimiter=',')
          file_o_csv.writerow(output)
          open_out.close()
      print('-' * 20 + 'end' + '-' * 20)
    process_log.pop()

driver.get(url)
# Wait for the panel-body element to be present in the DOM
WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.CLASS_NAME, "panel-body"))
)
brand_urls = [link.get_attribute('href') for link in driver.find_element(By.CLASS_NAME, 'panel-body').find_elements(By.TAG_NAME, 'a')]
print(f'Brand Number: {len(brand_urls)}')
if len(brand_urls):
  for index, brand_url in enumerate(brand_urls):
    print('***** Brand URL: ', brand_url)
    
    # load log info
    if os.path.isfile('C:\\Users\\rahul\\Documents\\Work\\7_impact\\2.0\\log.txt'):
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
    contents1 = [link.get_attribute('href') for link in driver.find_element(By.CLASS_NAME, 'content-box-1').find_elements(By.TAG_NAME, 'a')]
    print(f'Content Number: {len(contents1)}')
    get_items(contents1)
    process_log.pop()
    print('^' * 20 + 'NEXT BRAND' + '^' * 20)
  print('#' * 20 + 'Finish' + '#' * 20)
driver.quit()