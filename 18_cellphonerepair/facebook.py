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

service = Service(executable_path="C:\chromedriver-win64\chromedriver.exe")   
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9001")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
# driver.get('https://www.blisscomputers.net/')

# html_content = driver.page_source
# with open("output.html", "w", encoding="utf-8") as file:
#     file.write(html_content)

# sleep(random.uniform(1.0, 2.0))
# driver.find_element(By.ID, 'email').send_keys('chanddr@hotmail.com')
# driver.find_element(By.ID, 'pass').send_keys('1lincoln*')
# driver.find_element(By.ID, 'loginbutton').click()
# sleep(random.uniform(3.0, 5.0))

with open('urls.csv', 'r+', encoding='utf-8') as urls:
  all_urls = urls.readlines()

for url_index, url in enumerate(all_urls):
  driver.get(url)
  print(f'----- {url_index}th link -----')
  sleep(random.uniform(3.0, 5.0))
  output = []
  
  # location
  try:
    location = driver.find_elements(By.CLASS_NAME, 'x7wzq59')[1].find_elements(By.CSS_SELECTOR, '.xieb3on ul>div')[1].text
  except:
    location = ''
    
  # email
  try:
    email = driver.find_elements(By.CLASS_NAME, 'x7wzq59')[1].find_elements(By.CSS_SELECTOR, '.xieb3on ul>div')[3].text
  except:
    email = ''
    
  # phone_number
  try:
    phone_number = driver.find_elements(By.CLASS_NAME, 'x7wzq59')[1].find_elements(By.CSS_SELECTOR, '.xieb3on ul>div')[2].text
  except:
    phone_number = ''
  
  output.append(url)
  output.append(location)
  output.append(email)
  output.append(phone_number)
  print(output)
  
  open_out = open('output_cpr.csv','a',newline="", encoding='utf-8')
  file_o_csv = csv.writer(open_out, delimiter=',')
  file_o_csv.writerow(output)
  open_out.close()
print('*' * 20 + 'finish' + '*' * 20)