from bs4 import BeautifulSoup
import requests, csv
import os

url = 'https://www.aliexpress.com/w/wholesale-Replacement-laptop-lcd-led-screen-display.html?page=60&g=y&SearchText=Replacement+laptop+lcd+led+screen+display'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
print(soup.prettify)

with open("webpage.html", "w", encoding="utf-8") as file:
  file.write(soup.prettify)