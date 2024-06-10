# scrap by price

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

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9200")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def scrape_page(low, high):
  global item_num
  item_seg_num = 0
  page_id = 1
  is_last = False
  product_num = int(driver.find_element(By.CLASS_NAME, 's-desktop-toolbar').text.split('results')[0].strip().split(' ')[-1].replace(',', ''))
  print(f'There are over {product_num} products in {low}-{high} segment.\n')
  while not is_last:
    print(f'##### {page_id} Page/{low}-{high}/{product_num} #####')
    page_id += 1
    try:
      if driver.find_element(By.CLASS_NAME, 's-pagination-strip').find_elements(By.TAG_NAME, 'span')[-1].text.strip() == 'Next':
        is_last = True
      else:
        product_next_page_url = driver.find_element(By.CLASS_NAME, 's-pagination-strip').find_elements(By.TAG_NAME, 'a')[-1].get_attribute('href')
    except:
      is_last = True
    item_urls = []
    product_items = driver.find_elements(By.CSS_SELECTOR, '.s-widget-spacing-small:not(.AdHolder)')
    for product_item in product_items:
      item_urls.append(product_item.find_element(By.CSS_SELECTOR, '.s-product-image-container a').get_attribute('href'))
    for item_url in item_urls:
      driver.get(item_url)
      sleep(random.uniform(0.1, 0.2))
      
      while True:
        try:
          amazon_logo = driver.find_element(By.ID, 'nav-logo-sprites')
          break
        except:
          driver.refresh
          print('loading...')
          sleep(random.uniform(1, 2))
      
      # title
      try:
        item_title = driver.find_element(By.ID, 'productTitle').text
      except:
        continue
      if 'board' in item_title.lower() or 'circuit board' in item_title.lower() or 'battery' in item_title.lower() or 'keyboard' in item_title.lower() or 'desktop' in item_title.lower() or 'antenna' in item_title.lower() or 'wifi' in item_title.lower() or 'front cover' in item_title.lower() or 'back cover' in item_title.lower() or 'bottom base' in item_title.lower() or 'heatsink' in item_title.lower() or 'ac adapter' in item_title.lower() or 'ribbon' in item_title.lower() or 'cable' in item_title.lower() or 'bezel' in item_title.lower() or 'hinge' in item_title.lower() or 'cover' in item_title.lower() or 'screw' in item_title.lower() or 'hng' in item_title.lower() or 'powervault' in item_title.lower() or 'inverter' in item_title.lower() or 'invrtr' in item_title.lower() or 'cbl' in item_title.lower() or 'bzl' in item_title.lower() or 'mobile' in item_title.lower() or 'webcam' in item_title.lower() or 'phone' in item_title.lower() or 'touchpad' in item_title.lower() or 'protector' in item_title.lower():
        continue
      elif 'tape' in item_title.lower() or 'tool' in item_title.lower():
        if 'with' in item_title.lower():
          item_num += 1
          item_seg_num += 1
          # price
          try:
            item_price = driver.find_element(By.ID, 'corePrice_feature_div').text.replace('\n', '.')
          except:
            try:
              item_price = driver.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]').text.replace('\n', '.')
            except:
              item_price = ''
          
          output = [item_url, item_title, item_price]
          
          print(f'----- {item_num}/{item_seg_num} -----')
          # print(output)
          
          open_out = open(f'#amazon_jonas_{datetime.now().strftime("%Y-%m-%d")}_{low}-{high}_{product_num}.csv','a',newline="", encoding='utf-8-sig')
          file_o_csv = csv.writer(open_out, delimiter=',')
          file_o_csv.writerow(output)
          open_out.close()
        else:
          continue
      else:
        # price
        item_num += 1
        item_seg_num += 1
        try:
          item_price = driver.find_element(By.ID, 'corePrice_feature_div').text.replace('\n', '.')
        except:
          try:
            item_price = driver.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]').text.replace('\n', '.')
          except:
            item_price = ''
        
        output = [item_url, item_title, item_price]
        
        print(f'----- {item_num}/{item_seg_num} -----')
        # print(output)
        
        open_out = open(f'#amazon_jonas_{datetime.now().strftime("%Y-%m-%d")}_{low}-{high}_{product_num}.csv','a',newline="", encoding='utf-8-sig')
        file_o_csv = csv.writer(open_out, delimiter=',')
        file_o_csv.writerow(output)
        open_out.close()
        
      if item_num % 1000 == 0:
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        driver.execute_script("window.indexedDB.deleteDatabase('websql');")
        driver.refresh
    
    if not is_last:
      driver.get(product_next_page_url)

item_num = 1143
low_price = 26
high_price = 28
price_interval = 2

url = f'https://www.amazon.com/s?k=laptop+replacement+screens&rh=n%3A3011391011%2Cn%3A2612045011&dc&crid=1AX23ZA34FITZ&qid=1638896574&rnid=2941120011&sprefix=replacement+screens%2Caps%2C141&ref=sr_nr_n_2'
driver.get(url)

product_num = int(driver.find_element(By.CLASS_NAME, 's-desktop-toolbar').text.split('results')[0].strip().split(' ')[-1].replace(',', ''))
print(f'There are over {product_num} products.')

if(product_num > 9600):
  while(True):
    print(f'\n***** low_{(str(low_price) if low_price is not None else "")} - high_{str(high_price) if high_price is not None else ""} *****')
    
    driver.get(f'{url}&low-price={(str(low_price) if low_price is not None else "")}&high-price={(str(high_price) if high_price is not None else "")}')
    scrape_page(str(low_price) if low_price is not None else "", str(high_price) if high_price is not None else "")
    
    if high_price == None:
      break
    
    low_price = high_price
    high_price = round(high_price + price_interval, 1)
    
    if high_price >= 80 and high_price < 150:
      price_interval = 1
      if int(high_price % 10) == 9:
        price_interval = 0.1
    elif high_price >= 150 and high_price < 330:
      price_interval = 10
    elif high_price > 330:
      high_price = None
else:
  scrape_page()
print('^^^^^ Finish ^^^^^')