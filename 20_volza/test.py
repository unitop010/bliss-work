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

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = 'https://www.volza.com/p/lcd-panel-for-laptop/import/#/'
driver.get(url)
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ant-table-column-sorter-full')))
sortBtn = driver.find_elements(By.CLASS_NAME, 'ant-table-thead')[0].find_elements(By.TAG_NAME, 'th')[0]
sortBtn.click()
print('clicked')