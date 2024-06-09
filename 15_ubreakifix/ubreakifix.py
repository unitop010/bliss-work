from bs4 import BeautifulSoup
import requests, csv
import os

url = 'https://www.ubreakifix.com/locations'
process_log = []

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup.prettify)

location_blocks = soup.find_all('div', class_ = 'panel-default')
for location_block in location_blocks:
  location_items = location_block.find_all('div', class_ = 'panel-collapse')
  for location_item in location_items:
    locations = location_item.find_all('strong')
    for location in locations:
      location_email = location.text.replace(' ', '').replace('"', '').replace(',','').replace("'",'').lower() + '@ubreakifix.com'
      
      output = []    
      
      output.append(location.text)
      output.append(location_email)
      
      print(output)
      
      open_out = open('output.csv','a',newline="", encoding='utf-8')
      file_o_csv = csv.writer(open_out, delimiter=',')
      file_o_csv.writerow(output)
      open_out.close()