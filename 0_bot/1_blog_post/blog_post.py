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
from datetime import datetime
import json, csv, random, os, sys

service = Service(executable_path="C:\chromedriver-win64\chromedriver.exe")   
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9050")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# sleep(random.uniform(1.0, 2.0))
# driver.find_element(By.ID, 'email').send_keys('chanddr@hotmail.com')
# driver.find_element(By.ID, 'pass').send_keys('1lincoln*')
# driver.find_element(By.ID, 'loginbutton').click()
# sleep(random.uniform(3.0, 5.0))

with open('urls.csv', 'r+', encoding='utf-8') as urls:
  all_urls = urls.readlines()

output_directory = f'{datetime.now().strftime("%m_%d_%Y")}-{len(all_urls)}'

if not os.path.exists(output_directory):
  os.makedirs(output_directory)

for url_index, url in enumerate(all_urls):
  driver.get(url)
  sleep(random.uniform(3.0, 5.0))
  html_content = driver.page_source
  with open(f'{output_directory}/{url_index + 1}.html', "w", encoding="utf-8") as file:
    file.write(html_content)
  print(f'{url_index + 1}.html saved')
print('-' * 3 + 'finish' + '-' * 3)