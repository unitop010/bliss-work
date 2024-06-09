from bs4 import BeautifulSoup
import requests, csv
import os

url = 'https://www.lpscreen.com/en_laptop/replacement-laptop-screens.html'
process_log = []

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
items_num = soup.find_all('span', class_ = 'toolbar-number')[-1].text
page_num = int(int(items_num)/20) + 1
print(f'^^^^^ Item Number: {items_num} / Page Number: {page_num} ^^^^^')

for id in range(1, page_num + 1):
  process_log.append(id)
  # load log info
  if os.path.isfile('E:\\Scraping\\usa_rahul\\work\\13_lpscreen\\log.txt'):
    with open('log.txt', 'r', encoding='utf-8') as log_in:
      if log_in:
        log_indexes = log_in.read().split('-')
      else:
        log_indexes = []
    if log_indexes != [''] and log_indexes != []:
      index_value = int(log_indexes[0])
      if id < index_value:
        process_log.pop()
        continue
      elif id == index_value:
        log_indexes.pop(0)
      else:
        log_indexes = []
    else:
      log_in.close()
  else:
    log_indexes = []
    
  print(f'##### {id} Page #####')
  page_url = url + f"?p={id}"
  response = requests.get(page_url)
  soup = BeautifulSoup(response.content, 'html.parser')
  product_items = soup.find('ol', class_='product-items').find_all('h2', class_='product-item-name')
  for index, product_item in enumerate(product_items):
    process_log.append(index)
    if log_indexes != [''] and log_indexes != []:
      index_value = int(log_indexes[0])
      if index < index_value:
        process_log.pop()
        continue
      else:
        log_indexes.pop(0)
    elif os.path.isfile('E:\\Scraping\\usa_rahul\\work\\13_lpscreen\\log.txt'):
      try:
        log_in.close()
      except:
        pass
      
    # save log info
    log_out = open('log.txt','w', encoding='utf-8')
    output_str = '-'.join(map(str, process_log))
    log_out.write(output_str)
    log_out.close()
    
    output = []
    print('-' * 10, index, '-' * 10)
    item_url = product_item.find('a')['href']
    item_response = requests.get(item_url)
    item_soup = BeautifulSoup(item_response.content, 'html.parser')
    
    # Title
    try:
      item_title = item_soup.find('h1', class_='page-title').text
    except:
      item_title = ''
      
    # SKU
    try:
      item_sku = item_soup.find('div',{'itemprop': 'sku'}).text
    except:
      item_sku = ''
      
    # Price
    try:
      item_price = item_soup.find('span', class_='price').text
    except:
      item_price = ''
      
    output.append(item_url)
    output.append(item_title)
    output.append(item_sku)
    output.append(item_price)
    output.append('Replacement Laptop LCD LED Screen Display')
    
    print(output)
    
    open_out = open('output.csv','a',newline="", encoding='utf-8')
    file_o_csv = csv.writer(open_out, delimiter=',')
    file_o_csv.writerow(output)
    open_out.close()
    process_log.pop()
  process_log.pop()
print('*' * 20 + 'finish' + '*' * 20)