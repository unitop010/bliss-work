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
from time import sleep
import pandas as pd
import csv, os

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def remove_duplications():
  # Remove duplicated rows
  df = pd.read_csv(f'output_LG.csv')
  os.remove('output_LG.csv')
  df_unique = df.drop_duplicates()
  df_unique.to_csv('output_LG.csv', index=False, encoding='utf-8-sig')

states = ['ACTIVE', 'DISCONTINUED']
for state in states:
  print(f'*** {state} ***')
  page_id = 1
  while True:
    base_url = f'https://www.lg.com/us/support/warranty-information#subcat=lap&cat=computers&page={page_id}&sort=0&side=b2c&ct=CT00000317&sp=&state='
    driver.get(base_url + state)
    sleep(1)

    product_items = driver.find_elements(By.CLASS_NAME, 'box-result-item')

    if product_items:
      print(f'--- {page_id} page ---')
    else:
      print('else')
      break
    for product_item in product_items:
      # name
      try:
        product_name = product_item.find_element(By.CLASS_NAME, 'name').text
      except:
        product_name = ''
      # model number
      try:
        product_model = product_item.find_element(By.CLASS_NAME, 'model-number').text
      except:
        product_model = ''
      
      output = [product_name, product_model]
      
      open_out = open('output_LG.csv','a',newline="", encoding='utf-8-sig')
      file_o_csv = csv.writer(open_out, delimiter=',')
      file_o_csv.writerow(output)
      open_out.close()
    page_id += 1
print('-' * 5 + 'Scraping Finished' + '-' * 5)
driver.quit()