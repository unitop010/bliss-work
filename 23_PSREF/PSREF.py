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
import random

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def get_urls():
  products = driver.find_elements(By.CSS_SELECTOR, '#Laptops .productname_li')
  product_urls = []
  for product in products:
    product_url = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
    product_urls.append(product_url)
  print(f'{len(product_urls)} products found')
  return product_urls

def main(url):
  driver.get(url)
  products_urls = get_urls()
  for product_url in products_urls:
    driver.get(product_url)
    driver.find_element(By.ID, 'pro_ul_nav').find_elements(By.CLASS_NAME, 'tabnav')[1].click()
    driver.find_element(By.CSS_SELECTOR, '.top_btn .export').click()
    sleep(random.uniform(0.5, 1.0))

base_url = 'https://psref.lenovo.com/'
main(base_url)
print('-' * 5 + 'Scraping Finished' + '-' * 5)
driver.quit()