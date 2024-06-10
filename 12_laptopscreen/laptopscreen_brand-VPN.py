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
import VPN

def remove_history():
  # driver.delete_all_cookies()
  driver.execute_script("window.localStorage.clear();")
  driver.execute_script("window.sessionStorage.clear();")
  driver.execute_script("window.indexedDB.deleteDatabase('websql');")

item_num = 0
process_log = []

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# options = uc.ChromeOptions() 
# options.headless = False
# driver = uc.Chrome(use_subprocess=True, options=options) 

driver.get('https://www.laptopscreen.com/English/brands/')
# sleep(300)

# Wait for the element to be present
wait = WebDriverWait(driver, 300)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'brands_only')))
# Once the element is present, find the nested elements
brand_items = element.find_elements(By.TAG_NAME, "a")

brand_json_urls = []
# brand_items = driver.find_element(By.CLASS_NAME, "brands_only").find_elements(By.TAG_NAME, "a")
print(f'##### Brand Number: {len(brand_items)}')
for brand_item in brand_items:
  brand_json_url = brand_item.get_attribute('href')
  brand_json_urls.append(brand_json_url)
for index, brand_url in enumerate(brand_json_urls):
  process_log.append(index)
  # load log info
  if os.path.isfile('E:\\Scraping\\usa_rahul\\work\\12_laptopscreen\\log_brand.txt'):
    with open('log_brand.txt', 'r', encoding='utf-8') as log_in:
      if log_in:
        log_indexes = log_in.read().split('-')
      else:
        log_indexes = []
    if log_indexes != [''] and log_indexes != []:
      index_value = int(log_indexes[0])
      if index < index_value:
        process_log.pop()
        continue
      elif index == index_value:
        log_indexes.pop(0)
        with open('output_brand.csv', 'r+', encoding='utf-8') as file:
          # Read all lines in the file
          lines = file.readlines()
          # Check if there are lines to remove
          if lines:
            # Remove the last line
            lines = lines[:-1]
            # Go to the beginning of the file
            file.seek(0)
            # Write the modified lines
            file.writelines(lines)
            # Truncate the file to the new size
            file.truncate()
      else:
        log_indexes = []
    else:
      log_in.close()
  else:
    log_indexes = []
  
  print("##### Brand URL:", brand_url)      
  driver.get(brand_url)
  
  try:
    series_items = driver.find_element(By.CLASS_NAME, "tbt-off-1").find_elements(By.TAG_NAME, "a")
    series_json_urls = []
    print(f'^^^^^ Series Number: {len(series_items)}')
    for series_item in series_items:
      series_json_url = series_item.get_attribute('href')
      series_json_urls.append(series_json_url)
    for index, series_url in enumerate(series_json_urls):
      process_log.append(index)
      if log_indexes != [''] and log_indexes != []:
        index_value = int(log_indexes[0])
        if index < index_value:
          process_log.pop()
          continue
        else:
          log_indexes.pop(0)
      elif os.path.isfile('E:\\Scraping\\usa_rahul\\work\\12_laptopscreen\\log_brand.txt'):
        log_in.close()
      
      print("^^^^^ Series URL:", series_url)
      driver.get(series_url)
      try:
        model_page_num = int(driver.find_element(By.CLASS_NAME, "paginator").find_elements(By.TAG_NAME, "li")[-2].text)
      except:
        model_page_num = 1
      print("***** Page Number", model_page_num)
      for id in range(1, model_page_num + 1):
        process_log.append(id)
        if log_indexes != [''] and log_indexes != []:
          index_value = int(log_indexes[0])
          if id < index_value:
            process_log.pop()
            continue
          else:
            log_indexes.pop(0)
        elif os.path.isfile('E:\\Scraping\\usa_rahul\\work\\12_laptopscreen\\log_brand.txt'):
          log_in.close()
        
        print(f'***** {id} Page *****')
        driver.get(f'{series_url}?pgn&page={id}')
        
        product_json_urls = []
        product_items = driver.find_element(By.CLASS_NAME, "models-list").find_elements(By.TAG_NAME, "a")
        for product_item in product_items:
          product_json_url = product_item.get_attribute('href')
          product_json_urls.append(product_json_url)
        for index, product_url in enumerate(product_json_urls):
          process_log.append(index)
          if log_indexes != [''] and log_indexes != []:
            index_value = int(log_indexes[0])
            if index < index_value:
              process_log.pop()
              continue
            else:
              log_indexes.pop(0)
          elif os.path.isfile('E:\\Scraping\\usa_rahul\\work\\12_laptopscreen\\log_brand.txt'):
            log_in.close()
          driver.get(product_url)
          # save log info
          log_out = open('log_brand.txt','w', encoding='utf-8')
          output_str = '-'.join(map(str, process_log))
          log_out.write(output_str)
          log_out.close()
          
          # start scraping
          output = []
          product_title = ''
          product_part = ''
          product_price = ''
          item_num = item_num + 1
          print('-' * 10, item_num, '-' * 10)
          print(process_log)
          try:
            product_title_text = driver.find_element(By.CLASS_NAME, "parent_style").text
            product_title = product_title_text.split('from')[0].strip()
          except:
            try:
              no_items_found = driver.find_element(By.CLASS_NAME, "text-status-green").text
              print("No Items Found")
              process_log.pop()
              continue
            except:
              sys.exit()
            product_title = ''
          try:
            product_part = product_title_text.split('Replacement')[0].strip()
          except:
            product_part = ''
          try:
            product_prices = driver.find_elements(By.CLASS_NAME, "price-box")
            product_price = product_prices[0].find_element(By.TAG_NAME, "b").text
            if len(product_prices) > 1:
              for product_price_text in product_prices:
                product_price_float = product_price_text.find_element(By.TAG_NAME, "b").text
                if float(product_price_float.replace('$', '').replace('USD', '')) < float(product_price.replace('$', '').replace('USD', '')):
                  product_price = product_price_float
          except:
            product_price = ''
          output.append(product_url)
          output.append(product_title)
          output.append(product_part)
          output.append(product_price)
          output.append('Replacement Laptop LCD LED Screen Display Monitor')
          
          print(output)
          # sleep(0.2)
          sleep(random.uniform(0.1, 0.5))
          open_out = open('output_brand.csv','a',newline="", encoding='utf-8')
          file_o_csv = csv.writer(open_out, delimiter=',')
          file_o_csv.writerow(output)
          open_out.close()
          process_log.pop()
          if item_num % 200 == 0:
            remove_history()
            VPN.change_ip()
            driver.refresh
        process_log.pop()
      process_log.pop()
  except:
    try:
      model_page_num = int(driver.find_element(By.CLASS_NAME, "paginator").find_elements(By.TAG_NAME, "li")[-2].text)
    except:
      model_page_num = 1
    print("***** Page Number", model_page_num)
    for id in range(1, model_page_num + 1):
      process_log.append(id)
      if log_indexes != [''] and log_indexes != []:
        index_value = int(log_indexes[0])
        if id < index_value:
          process_log.pop()
          continue
        else:
          log_indexes.pop(0)
      elif os.path.isfile('E:\\Scraping\\usa_rahul\\work\\12_laptopscreen\\log_brand.txt'):
        log_in.close()
      
      print(f'***** {id} Page *****')
      driver.get(f'{series_url}?pgn&page={id}')
      
      product_json_urls = []
      product_items = driver.find_element(By.CLASS_NAME, "models-list").find_elements(By.TAG_NAME, "a")
      for product_item in product_items:
        product_json_url = product_item.get_attribute('href')
        product_json_urls.append(product_json_url)
      for index, product_url in enumerate(product_json_urls):
        process_log.append(index)
        if log_indexes != [''] and log_indexes != []:
          index_value = int(log_indexes[0])
          if index < index_value:
            process_log.pop()
            continue
          else:
            log_indexes.pop(0)
        elif os.path.isfile('E:\\Scraping\\usa_rahul\\work\\12_laptopscreen\\log_brand.txt'):
          log_in.close()
        driver.get(product_url)
        # save log info
        log_out = open('log_brand.txt','w', encoding='utf-8')
        output_str = '-'.join(map(str, process_log))
        log_out.write(output_str)
        log_out.close()
        
        # start scraping
        output = []
        product_title = ''
        product_part = ''
        product_price = ''
        item_num = item_num + 1
        print('-' * 10, item_num, '-' * 10)
        print(process_log)
        try:
          product_title_text = driver.find_element(By.CLASS_NAME, "parent_style").text
          product_title = product_title_text.split('from')[0].strip()
        except:
          try:
            no_items_found = driver.find_element(By.CLASS_NAME, "text-status-green").text
            print("No Items Found")
            process_log.pop()
            continue
          except:
            sys.exit()
          product_title = ''
        try:
          product_part = product_title_text.split('Replacement')[0].strip()
        except:
          product_part = ''
        try:
          product_prices = driver.find_elements(By.CLASS_NAME, "price-box")
          product_price = product_prices[0].find_element(By.TAG_NAME, "b").text
          if len(product_prices) > 1:
            for product_price_text in product_prices:
              product_price_float = product_price_text.find_element(By.TAG_NAME, "b").text
              if float(product_price_float.replace('$', '').replace('USD', '')) < float(product_price.replace('$', '').replace('USD', '')):
                product_price = product_price_float
        except:
          product_price = ''
        output.append(product_url)
        output.append(product_title)
        output.append(product_part)
        output.append(product_price)
        output.append('Replacement Laptop LCD LED Screen Display')
        
        print(output)
        # sleep(0.2)
        sleep(random.uniform(0.1, 0.5))
        open_out = open('output_brand.csv','a',newline="", encoding='utf-8')
        file_o_csv = csv.writer(open_out, delimiter=',')
        file_o_csv.writerow(output)
        open_out.close()
        process_log.pop()
        if item_num % 200 == 0:
          remove_history()
          VPN.change_ip()
          driver.refresh
      process_log.pop()
  process_log.pop()
print('*' * 20 + 'finish' + '*' * 20)