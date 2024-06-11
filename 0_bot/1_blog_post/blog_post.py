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

service = Service(executable_path="C:\chromedriver-win64\chromedriver.exe")   
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9050")
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-gpu")  # applicable to windows os only
chrome_options.add_argument("start-maximized")  # open Browser in maximized mode
chrome_options.add_argument("disable-infobars")  # disabling infobars
chrome_options.add_argument("--disable-extensions")  # disabling extensions
chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# sleep(random.uniform(1.0, 2.0))
# driver.find_element(By.ID, 'email').send_keys('chanddr@hotmail.com')
# driver.find_element(By.ID, 'pass').send_keys('1lincoln*')
# driver.find_element(By.ID, 'loginbutton').click()
# sleep(random.uniform(3.0, 5.0))

with open('urls.csv', 'r+', encoding='utf-8') as urls:
  all_urls = urls.readlines()

for url_index, url in enumerate(all_urls):
  driver.get(url)
  html_content = driver.page_source
  with open("output.html", "w", encoding="utf-8") as file:
    file.write(html_content)
print('*' * 20 + 'finish' + '*' * 20)