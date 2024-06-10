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
import json, csv, random, os, sys

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9001")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

item_num = 0
page_id = 1
is_last = False
while not is_last:
  url = f'https://www.amazon.com/s?i=merchant-items&me=AAV24S8U9I601&page={page_id}&marketplaceID=ATVPDKIKX0DER&qid=1715535352&ref=sr_pg_{page_id}'
  driver.get(url)
  print(f'##### {page_id} Page #####')
  page_id += 1
  if driver.find_element(By.CLASS_NAME, 's-pagination-strip').find_elements(By.TAG_NAME, 'span')[-1].text.strip() == 'Next':
    is_last = True
  item_urls = []
  product_items = driver.find_elements(By.CLASS_NAME, 's-widget-spacing-small')
  for product_item in product_items:
    item_urls.append(product_item.find_element(By.TAG_NAME, 'a').get_attribute('href'))
  for item_url in item_urls:
    driver.get(item_url)
    sleep(random.uniform(0.1, 0.5))
    item_num += 1
    # title
    try:
      item_title = driver.find_element(By.ID, 'productTitle').text
    except:
      item_title = ''
    # price
    try:
      item_price = driver.find_element(By.ID, 'corePrice_feature_div').text.replace('\n', '.')
    except:
      item_price = ''
    # part number & model
    item_part = ''
    item_model = ''
    try:
      item_descriptions = driver.find_element(By.ID, 'productDetails_detailBullets_sections1').find_elements(By.TAG_NAME, 'tr')
      for item_description in item_descriptions:
        if item_description.text.lower().strip().startswith('asin'):
          item_part = item_description.text.removeprefix('ASIN').strip()
        elif item_description.text.lower().strip().startswith('item model number'):
          item_model = item_description.text.removeprefix('Item model number').strip()
    except:
      pass
    
    output = []
    output.append(item_url)
    output.append(item_title)
    output.append('Replacement Laptop LCD LED Screen Display Monitor')
    output.append(item_part)
    output.append(item_model)
    output.append(item_price)
    
    print(f'----- {item_num} -----')
    print(output)
    
    open_out = open('output_amazon.csv','a',newline="", encoding='utf-8')
    file_o_csv = csv.writer(open_out, delimiter=',')
    file_o_csv.writerow(output)
    open_out.close()
print('^^^^^ Finish ^^^^^')