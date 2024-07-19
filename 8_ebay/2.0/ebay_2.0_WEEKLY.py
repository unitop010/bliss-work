from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from datetime import datetime
import requests, csv, math, random, os

item_num = 0
process_log = []
directory = f'{datetime.now().strftime("%m-%d-%Y")}_WEEKLY'
primary_directory = f'output_{directory}'

# if not os.path.exists(directory):
#   os.makedirs(directory)

if not os.path.exists(primary_directory):
  os.makedirs(primary_directory)

urls = open('urls_WEEKLY.csv', 'r+',  encoding='latin-1')
all_urls = csv.reader(urls)
with open('unnecessary_keywords.csv', 'r+', encoding='utf-8') as keywords:
  all_keywords = keywords.readlines()

def save_csv(id, page_soup, id_index):
  global primary_directory, item_num
  
  page_items = page_soup.find('ul', class_='srp-results').find_all('li', class_='s-item__pl-on-bottom')
  for page_item in page_items:
    item_url = page_item.find('a', class_='s-item__link')['href']
    item_title = page_item.find('div', class_='s-item__title').text
    item_base_price_text = page_item.find('span', class_='s-item__price').text
    item_currency = '$'
    if 'AU $' in item_base_price_text:
      item_currency = 'AU $'
      item_currency_rate = 0.68
    elif '$' in item_base_price_text:
      item_currency = '$'
      item_currency_rate = 1
    elif '£' in item_base_price_text:
      item_currency = '£'
      item_currency_rate = 1.28
    item_base_price = float(item_base_price_text.split('to')[0].strip().replace(item_currency, '').replace(',', ''))
    try:
      item_shipping_price_text = page_item.find('span', class_='s-item__shipping').text.lower()
      if '+' in item_shipping_price_text and item_currency in item_shipping_price_text:
        item_shipping_price = float(item_shipping_price_text.split(' ')[0].replace('+', '').replace(item_currency, '').replace(',', ''))
      else:
        item_shipping_price = 0
    except:
      item_shipping_price = 0
    item_price = round((item_base_price + item_shipping_price) * item_currency_rate, 2)
    if any(keyword.strip() in item_title.lower() for keyword in all_keywords):
      continue
    elif 'tape' in item_title.lower():
      if 'tool' in item_title.lower():
        item_num += 1
        output = [item_title, item_price]
        open_out = open(f'{primary_directory}/{id_index}-#ebay_{id}_jonas.csv','a',newline="", encoding='utf-8-sig')
        file_o_csv = csv.writer(open_out, delimiter=',')
        file_o_csv.writerow(output)
        open_out.close()
      else:
        continue
    else:
      item_num += 1
      output = [item_title, item_price]
      open_out = open(f'{primary_directory}/{id_index}-#ebay_{id}_jonas.csv','a',newline="", encoding='utf-8-sig')
      file_o_csv = csv.writer(open_out, delimiter=',')
      file_o_csv.writerow(output)
      open_out.close()
  print(f'          {item_num} products scraped')

def scrape_id(id, id_url, id_index, id_product_num):
  id_url = f'{id_url}&_ipg=240'
  # verify pagination
  if id_product_num > 240:
    page_id = 1
    while True:
      if page_id > 42:
        break
      print(f'----- {id_index} : {id}({id_product_num}) / {page_id} page -----')
      page_url = f'{id_url}&_pgn={page_id}'
      page_id_response = requests.get(page_url)
      page_id_soup = BeautifulSoup(page_id_response.content, 'html.parser')
      try:
        id_pagination = page_id_soup.find('div', class_='s-pagination').find('nav')
      except:
        break
      save_csv(id, page_id_soup, id_index)
      try:
        is_last_button = id_pagination.find_all('a')[-1]['aria-label']
        page_id += 1
      except:
        break
  else: # item numbers less than 240
    id_response = requests.get(id_url)
    id_soup = BeautifulSoup(id_response.content, 'html.parser')
    save_csv(id, id_soup, id_index)

def data_process():
  global directory, primary_directory
  # Merge csv files
  csv_files = [file for file in os.listdir(primary_directory) if file.endswith('.csv')]
  print(f"\n----- Found {len(csv_files)} CSV files in the directory '{primary_directory}' -----")
  dataframes_list = []
  for csv_file in csv_files:
    file_path = os.path.join(primary_directory, csv_file)
    df = pd.read_csv(file_path, header=None)  # Read without headers
    dataframes_list.append(df)
  merged_df = pd.concat(dataframes_list, ignore_index=True)
  merged_df.columns = ['Title', 'Price']
  print("***** All CSV files merged *****")
  
  # Remove duplications
  df_unique = merged_df.drop_duplicates(subset=['Title'])
  print("\n***** All duplications removed *****")

  # Save csv file
  df_unique.to_csv(f'{primary_directory}/#ebay_Jonas_{directory}.csv', index=False, encoding='utf-8-sig')
  print(f'\n***** CSV files saved in {primary_directory} *****\n')
  
  # Split the DataFrame into smaller DataFrames with 10000 rows each
  # dfs = [df_unique[i:i+10000] for i in range(0, len(df_unique), 10000)]
  # for i, smaller_df in enumerate(dfs):
  #   smaller_df.to_csv(f'{directory}/#ebay_Jonas_{directory}_{i + 1}.csv', index=False, encoding='utf-8-sig')
  # print(f'\n***** CSV files saved in {directory} *****\n')

for url_index, url in enumerate(all_urls):
  id_index = url_index + 1
  response = requests.get(f'{url[0]}&_udlo=25')
  soup = BeautifulSoup(response.content, 'html.parser')
  # html_content = str(soup.prettify)
  # with open("webpage.html", "w", encoding="utf-8") as file:
  #   file.write(html_content)
  product_num = int(soup.find('h1', class_='srp-controls__count-heading').text.split(' ')[0].replace('+', '').replace(',', ''))
  print(f'\n***** {id_index} : "{url[1]}" has about {product_num} items *****')
  if product_num == 0:
    continue
  if product_num > 10000:
    product_seg = math.floor(product_num/10000)
    price_low = 25
    price_high = 50
    price_interval = 5
    while True:
      price_high += price_interval
      price_url = f'{url[0]}&_udhi={price_high}&_udlo={price_low}'
      price_response = requests.get(price_url)
      price_soup = BeautifulSoup(price_response.content, 'html.parser')
      price_product_num =  int(price_soup.find('h1', class_='srp-controls__count-heading').text.split(' ')[0].replace('+', '').replace(',', ''))
      if price_product_num > 10000:
        price_high -= price_interval
        product_seg -= 1
        print(f'~~~~~ {url[1]} / {price_low} - {price_high} ~~~~~')
        scrape_id(url[1], f'{url[0]}&_udhi={price_high}&_udlo={price_low}', id_index, price_product_num)
        price_low = price_high
      if product_seg == 0:
        print(f'~~~~~ {url[1]} / {price_low} - ~~~~~')
        scrape_id(url[1], f'{url[0]}&_udlo={price_low}', id_index, price_product_num)
        break
      sleep(random.uniform(1, 2))
  else:
    scrape_id(url[1], f'{url[0]}&_udlo=25', id_index, product_num)
urls.close()
print('\n***** Scraping finished *****')
data_process()