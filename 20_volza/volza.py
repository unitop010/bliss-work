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

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
click_sort_id = 0

def get_listings():
  infos = driver.find_elements(By.CLASS_NAME, 'ant-table-body')[0].find_element(By.CLASS_NAME, 'ant-table-tbody').find_elements(By.TAG_NAME, 'tr')
  for info_id in range(1, len(infos)):
    description = ''
    description = infos[info_id].find_elements(By.TAG_NAME, 'td')[1].text
    
    output = []
    output.append(description)  
    open_out = open('output.csv','a',newline="", encoding='utf-8')
    file_o_csv = csv.writer(open_out, delimiter=',')
    file_o_csv.writerow(output)
    open_out.close()

def clickSort():
  global click_sort_id
  while click_sort_id < 4:
    click_sort_id = click_sort_id + 1
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ant-table-column-sorter-full')))
    sortBtn = driver.find_elements(By.CLASS_NAME, 'ant-table-thead')[0].find_elements(By.TAG_NAME, 'th')
    get_listings()
    sortBtn[click_sort_id].click()
    get_listings()
    sortBtn[click_sort_id].click()
    get_listings()
    driver.refresh()

def main(url):
  global click_sort_id
  driver.get(url)
  print(f'HSN link : {url}')
  clickSort()
  click_sort_id = 0
  hsn_urls = driver.find_elements(By.CLASS_NAME, 'common-scrollbar-globalFilters')[0].find_elements(By.TAG_NAME, 'a')
  hsn_hrefs = []
  for hsn_url in hsn_urls:
    hsn_href = hsn_url.get_attribute('href')
    hsn_hrefs.append(hsn_href)
  if len(hsn_urls) > 1:
    for hsn_href in hsn_hrefs:
      main(hsn_href)

base_url = 'https://www.volza.com/p/lcd-panel-for-laptop/import/#/'
main(base_url)
print('-' * 5 + 'Scraping Finished' + '-' * 5)
driver.quit()