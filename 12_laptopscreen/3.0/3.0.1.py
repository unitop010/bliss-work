import requests, csv, random, json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent
from time import sleep
import pandas as pd

base_url = 'https://www.laptopscreen.com/English/'

ua = UserAgent()

headers = {
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  # "Accept-Encoding": "gzip, deflate, br, zstd",
  "Accept-Language": "en-US,en;q=0.9",
  "Cookie": "PHPSESSID=gp3pdvle3g5lvcm4qbb3vnb827; cartId=cart24_66976aadd76b52.10394378; Currency=USD; Lang=English; __zlcmid=1MnmsGbk3cII6le; logUserId=66976aadd91213.18391796; logRecordId=15397562; cfzs_google-analytics_v4=%7B%22MDRR_pageviewCounter%22%3A%7B%22v%22%3A%223%22%7D%7D; cfz_google-analytics_v4=%7B%22MDRR_engagementDuration%22%3A%7B%22v%22%3A%220%22%2C%22e%22%3A1752735400925%7D%2C%22MDRR_engagementStart%22%3A%7B%22v%22%3A%221721199400925%22%2C%22e%22%3A1752735400925%7D%2C%22MDRR_counter%22%3A%7B%22v%22%3A%223%22%2C%22e%22%3A1752735400925%7D%2C%22MDRR_ga4sid%22%3A%7B%22v%22%3A%221205840012%22%2C%22e%22%3A1721201200925%7D%2C%22MDRR_session_counter%22%3A%7B%22v%22%3A%221%22%2C%22e%22%3A1752735400925%7D%2C%22MDRR_ga4%22%3A%7B%22v%22%3A%229b291b43-27f5-4dd9-9b5d-94c701fffbbb%22%2C%22e%22%3A1752735400925%7D%2C%22MDRR__z_ga_audiences%22%3A%7B%22v%22%3A%229b291b43-27f5-4dd9-9b5d-94c701fffbbb%22%2C%22e%22%3A1752735280211%7D%2C%22MDRR_let%22%3A%7B%22v%22%3A%221721199400925%22%2C%22e%22%3A1752735400925%7D%7D",
  "Priority": "u=0, i",
  "Referer": "https://www.google.com/",
  "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
  "Sec-Ch-Ua-Mobile": "?0",
  "Sec-Ch-Ua-Platform": "\"Windows\"",
  "Sec-Fetch-Dest": "document",
  "Sec-Fetch-Mode": "navigate",
  "Sec-Fetch-Site": "same-origin",
  "Sec-Fetch-User": "?1",
  "Upgrade-Insecure-Requests": "1",
  # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
  "User-Agent": str(ua.random)
}

def scrape_page(page_index, page_soup):
  try:
    page_products_listings = page_soup.find_all(class_='models-list')
    for page_products_listing in page_products_listings:
      page_products = page_products_listing.find_all('a')
      for page_product in page_products:
        # sleep(random.uniform(2, 4))
        # product_url = urljoin(base_url, page_product['href'])
        product_url = page_product['href'].text.replace('\n', '')
        
        # product_response = requests.get(product_url, headers=headers)
        # product_soup = BeautifulSoup(product_response.content, 'html.parser')
        # products = product_soup.find('main').find_all(class_='item-box')
        # for product in products:
        #   output = []
        #   item_comp = ''
        #   item_size = ''
        #   item_resol = ''
        #   item_connector = ''
        #   item_rate = ''
          
        #   product_specs = product.find(class_='spec-table').find_all(class_='row')
        #   for product_spec in product_specs:
        #     product_spec_text = product_spec.text.replace('\n', '')
        #     if product_spec_text.startswith('Compatibility:'):
        #       item_comp = product_spec_text.replace('Compatibility:', '').replace('SERIES', '').strip() + ' '
        #     elif product_spec_text.startswith('Size:'):
        #       item_size = product_spec_text.replace('Size:', '').split('"')[0].strip() + '" '
        #     elif product_spec_text.startswith('Resolution:'):
        #       item_resol = product_spec_text.replace('Resolution:', '').strip() + ' '
        #     elif product_spec_text.startswith('Video Connector:'):
        #       item_connector = product_spec_text.replace('Video Connector:', '').replace('video connector', '').strip() + 's '
        #     elif product_spec_text.startswith('Refresh Rate:'):
        #       item_rate = product_spec_text.replace('Refresh Rate:', '').strip() + ' '
        #   item_title = (item_comp + item_size + item_resol + item_connector + item_rate + 'Non Touch Replacement Screen Display').replace('\n', '')
        #   output = [item_title, item_comp.strip(), item_size.strip(), item_resol.strip(), item_connector.strip(), item_rate.strip()]
        #   print('  ' * 3 + f'{page_index}: ' + item_title)
        #   with open('output.csv', 'a', newline="", encoding='utf-8-sig') as file:
        #     file_o_csv = csv.writer(file, delimiter=',')
        #     file_o_csv.writerow(output)
        
        output = [product_url]
        with open(output_file, 'a', newline="", encoding='utf-8-sig') as file:
          file_o_csv = csv.writer(file, delimiter=',')
          file_o_csv.writerow(output)
    print('  ' * 3 + f'{page_index}')
  except:
    print('  ' * 3 + f'{page_index}: No products')
    sleep(random.uniform(2, 4))

def scrape_series(series_index, series_url, series_soup):
  try:
    page_num = int(series_soup.find(class_='paginator').find_all('li')[-2].text)
    print('  ' * 2 + f'{page_num} pages')
    for page_id in range(1, page_num + 1):
      sleep(random.uniform(2, 4))
      page_url = series_url + f'?pgn&page={page_id}'
      page_response = requests.get(page_url, headers=headers)
      page_soup = BeautifulSoup(page_response.content, 'html.parser')
      scrape_page(f'{series_index}/{page_id} page', page_soup)
  except:
    print('  ' * 2 + 'No pages...')
    scrape_page(series_index, series_soup)

# Write csv file header
output_file = 'output_urls.csv'
# csv_header = ['Title', 'Compatibility', 'Size', 'Resolution', 'Video Connector', 'Refresh Rate']
csv_header = ['URL']
try:
  with open(output_file, 'r') as file:
    pass
except FileNotFoundError:
  with open(output_file, 'a', newline='') as file:
    file_o_csv = csv.writer(file)
    file_o_csv.writerow(csv_header)

response = requests.get(base_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

brands = soup.find(class_='inventory-list').find_all('a')
print(f'### Brand: {len(brands)} brands\n')
for brand_index, brand in enumerate(brands):
  sleep(random.uniform(2, 4))
  brand_url = urljoin(base_url, brand['href'])
  print(f'### Brand/{brand_index + 1}: {brand_url}')
  if brand_index + 1 < 8:
    continue
  brand_response = requests.get(brand_url, headers=headers)
  brand_soup = BeautifulSoup(brand_response.content, 'html.parser')
  
  try:
    brand_series_items = brand_soup.find(class_='tbt-off-1').find_all('a')
    print(f'^^^ Series/{brand_index + 1}: {len(brand_series_items)} series')
    for series_index, series_item in enumerate(brand_series_items):
      sleep(random.uniform(2, 4))
      series_url = urljoin(base_url, series_item['href'])
      print(f'^^^ Series/{brand_index + 1}/{series_index + 1}: {series_url}')
      series_response = requests.get(series_url, headers=headers)
      series_soup = BeautifulSoup(series_response.content, 'html.parser')
      scrape_series(f'{brand_index + 1}/{series_index + 1}', series_url, series_soup)
  except:
    print('^^^ Series: No series...')
    scrape_series(f'{brand_index + 1}', brand_url, brand_soup)

# Remove duplications from csv file
df = pd.read_csv(output_file)
df_unique = df.drop_duplicates(subset=['Title'])
df_unique.to_csv('complete.csv', index=False, encoding='utf-8-sig')
print('-' * 5 + 'Finish' + '-' * 5)