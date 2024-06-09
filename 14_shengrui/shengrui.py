from bs4 import BeautifulSoup
import requests, csv
import os

url = 'https://www.shengruihk.com/product-category/lcd-with-touch-and-board-complete/'
process_log = []

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup.prettify)
page_num = soup.find('ul', class_ = 'page-numbers').find_all('li')[-2].text
print(f'^^^^^ Page Number: {page_num} ^^^^^')

for id in range(1, int(page_num) + 1):
  process_log.append(id)
  # load log info
  if os.path.isfile('E:\\Scraping\\usa_rahul\\work\\14_shengrui\\log.txt'):
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
  page_url = url + f"page/{id}/"
  response = requests.get(page_url)
  soup = BeautifulSoup(response.content, 'html.parser')
  product_items = soup.find_all('div', class_='product-grid-item')
  for index, product_item in enumerate(product_items):
    process_log.append(index)
    if log_indexes != [''] and log_indexes != []:
      index_value = int(log_indexes[0])
      if index < index_value:
        process_log.pop()
        continue
      else:
        log_indexes.pop(0)
    elif os.path.isfile('E:\\Scraping\\usa_rahul\\work\\14_shengrui\\log.txt'):
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
      item_title = item_soup.find('h1', class_='product_title').text
    except:
      item_title = ''
      
    # Price
    try:
      item_price = item_soup.find(class_='summary-inner').find('bdi').text
    except:
      item_price = ''
      
    # Model & Part No
    try:
      try:
        item_descriptions = item_soup.find('table', class_='tab1').text.split('\n')
        for index, item_description in enumerate(item_descriptions):
          if 'Display' in item_description:
            item_partNo = item_descriptions[index + 1]
            break
          else:
            item_partNo = ''
          
          if 'Compatib' in item_description:
            item_model = item_descriptions[index + 1]
            break
          else:
            item_model = ''
      except:
        item_descriptions = item_soup.find('div', class_='woocommerce-Tabs-panel').find_all('p')
        for item_description in item_descriptions:
          if 'Part Number' in item_description.text:
            item_partNo = item_description.text.split(':')[1].strip()
            break
          else:
            item_partNo = ''
          
          if 'Compatib' in item_description.text:
            item_model = item_description.text.split(':')[1].strip()
            break
          else:
            item_model = ''
    except:
      item_model = ''
      
    output.append(item_url)
    output.append(item_title)
    output.append(item_price)
    output.append(item_partNo)
    output.append(item_model)
    output.append('Replacement Laptop LCD LED Screen Display')
    
    print(output)
    
    open_out = open('output.csv','a',newline="", encoding='utf-8')
    file_o_csv = csv.writer(open_out, delimiter=',')
    file_o_csv.writerow(output)
    open_out.close()
    process_log.pop()
  process_log.pop()
print('*' * 20 + 'finish' + '*' * 20)