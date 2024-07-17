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
from bs4 import BeautifulSoup
import requests
import json, csv, random, os, sys

options = Options()
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9200")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.maximize_window()


with open('1.html', 'r', encoding='utf-8') as file:
  html_content = file.read()
soup = BeautifulSoup(html_content, 'html.parser')
urls = soup.find_all('a', class_ = 'link-no-decals')
for url in urls:
  driver.get(f'https://www.laptopscreen.com{url["href"]}')
  print(f'https://www.laptopscreen.com{url["href"]}')
  
  wait = WebDriverWait(driver, 300)
  element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'main')))
  items = element.find_elements(By.CLASS_NAME, 'item-box')
  
  for item in items:
    item_comp = ''
    item_size = ''
    item_resol = ''
    item_connector = ''
    item_rate = ''
    
    item_specs = item.find_element(By.CLASS_NAME, 'spec-table').text.split('\n')
    for i in range(len(item_specs)):
      if item_specs[i].startswith('Compatibility:'):
        item_comp = item_specs[i + 1].replace('SERIES', '').strip() + ' '
      elif item_specs[i].startswith('Size:'):
        item_size = item_specs[i + 1].replace('WideScreen', '').strip() + ' '
      elif item_specs[i].startswith('Resolution:'):
        item_resol = item_specs[i + 1] + ' '
      elif item_specs[i].startswith('Video Connector:'):
        item_connector = item_specs[i + 1].replace('video connector', '').strip() + 's '
      elif item_specs[i].startswith('Refresh Rate:'):
        item_rate = item_specs[i + 1] + ' '
    item_title = [(item_comp + item_size + item_resol + item_connector + item_rate + 'Non Touch Replacement Screen Display').replace('\n', '')]
    
    with open('GU603.csv', 'a', encoding='utf-8-sig') as file:
      file_o_csv = csv.writer(file, delimiter=',')
      file_o_csv.writerow(item_title)
  sleep(5)