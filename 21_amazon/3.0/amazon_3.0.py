import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import csv, random

main_url = 'https://www.amazon.com/s?k=laptop+replacement+screens&rh=n%3A3011391011%2Cn%3A2612045011&dc&crid=1AX23ZA34FITZ&qid=1638896574&rnid=2941120011&sprefix=replacement+screens%2Caps%2C141&ref=sr_nr_n_2'

headers = {
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  "Accept-Encoding": "gzip, deflate, br, zstd",
  "Accept-Language": "en,en-US;q=0.9",
  "Cookie": "session-id=142-2872587-8215045; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=132-4022569-5778914; JSESSIONID=BE4BB7F57F6D6E6C54B531B14CB0C4F6; session-token=NRH8KmEdTIipM52EDEevno33T6UKSIFR8n27a3IXqY6vqd+e15EF9gGu/zyUWmmoeVWAliwr6GKw8EhWIFdbphXVPO0eM3O17eMyiMm4Ng2c7XYYP48SwptWSamuEFBr/Z1n/in6az7IUS3ZVAjGjc73GAgK3Rs6/FyMD20ldyTI38U7iKcyf0WyqDe37Jrp5k24bSLPxy8M6NRhBCQ2JqfA6U89tORHm+pdm05Wz//qwuCvA0Jkn5FFpA3SpE2gmlMRqkXSsOSa8IlKoLyugg6zsIEhSRYvHgt9Y/s2lyozTRhVAwEVKlaz0QSsVnCBnGXazRuGVJDg4Jn2WtcJHxX3vq/QN9Ii; csm-hit=tb:Z1FV7D3CCMVVR2P32BB0+s-ZDCG0R1S0XDT462VBSJV|1719584365172&t:1719584365172&adb:adblk_yes",
  "Device-Memory": "8",
  "Downlink": "4.7",
  "Dpr": "1",
  "Ect": "4g",
  "Priority": "u=0, i",
  "Rtt": "150",
  "Sec-Ch-Device-Memory": "8",
  "Sec-Ch-Dpr": "1",
  "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
  "Sec-Ch-Ua-Mobile": "?0",
  "Sec-Ch-Ua-Platform": "\"Windows\"",
  "Sec-Ch-Ua-Platform-Version": "\"10.0.0\"",
  "Sec-Ch-Viewport-Width": "1920",
  "Sec-Fetch-Dest": "document",
  "Sec-Fetch-Mode": "navigate",
  "Sec-Fetch-Site": "none",
  "Sec-Fetch-User": "?1",
  "Upgrade-Insecure-Requests": "1",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
  "Viewport-Width": "1920"
}

def scrape_page(price_list):
  page_response = requests.get(f'{main_url}{price_list}', headers=headers)
  page_soup = BeautifulSoup(page_response.content, 'html.parser')
  
  try:
    page_num = page_soup.find(class_='s-pagination-strip').find_all('span', class_='s-pagination-item')[-1].text
    for page_id in range(1, int(page_num) + 1):
      print(f'----- {page_id} Page/{price_list} -----')
      scrape_products(f'https://www.amazon.com/s?k=laptop+replacement+screens&i=computers&rh=n%3A3011391011%2Cn%3A2612045011&dc&page={page_id}&crid=1AX23ZA34FITZ&qid=1719582574&refresh=1&rnid=2941120011&sprefix=replacement+screens%2Caps%2C141&ref=sr_pg_2{price_list}')
  except:
    scrape_products(f'{main_url}{price_list}')
    print(f'----- {price_list} -----')

def scrape_products(url):
  global item_num
  item_seg_num = 0
  
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, 'html.parser')
  
  product_items = soup.find_all(class_ = 's-widget-spacing-small')
  for product_item in product_items:
    item_title = product_item.find('div', attrs={'data-cy': 'title-recipe'}).text
    try:
      item_price = product_item.find('div', attrs={'data-cy': 'price-recipe'}).find(class_='a-offscreen').text
    except:
      item_price = ''
    
    if 'board' in item_title.lower() or 'circuit board' in item_title.lower() or 'battery' in item_title.lower() or 'keyboard' in item_title.lower() or 'desktop' in item_title.lower() or 'antenna' in item_title.lower() or 'wifi' in item_title.lower() or 'front cover' in item_title.lower() or 'back cover' in item_title.lower() or 'bottom base' in item_title.lower() or 'heatsink' in item_title.lower() or 'ac adapter' in item_title.lower() or 'ribbon' in item_title.lower() or 'cable' in item_title.lower() or 'bezel' in item_title.lower() or 'hinge' in item_title.lower() or 'cover' in item_title.lower() or 'screw' in item_title.lower() or 'hng' in item_title.lower() or 'powervault' in item_title.lower() or 'inverter' in item_title.lower() or 'invrtr' in item_title.lower() or 'cbl' in item_title.lower() or 'bzl' in item_title.lower() or 'mobile' in item_title.lower() or 'webcam' in item_title.lower() or 'phone' in item_title.lower() or 'touchpad' in item_title.lower() or 'protector' in item_title.lower():
      continue
    elif 'tape' in item_title.lower() or 'tool' in item_title.lower():
      if 'with' in item_title.lower():
        item_num += 1
        item_seg_num += 1
        output = [item_title, item_price]
        with open(f'#amazon_jonas_{datetime.now().strftime("%Y-%m-%d")}.csv', 'a', newline="", encoding='utf-8-sig') as open_out:
          file_o_csv = csv.writer(open_out, delimiter=',')
          file_o_csv.writerow(output)
      else:
        continue
    else:
      item_num += 1
      item_seg_num += 1
      output = [item_title, item_price]
      with open(f'#amazon_jonas_{datetime.now().strftime("%Y-%m-%d")}.csv', 'a', newline="", encoding='utf-8-sig') as open_out:
        file_o_csv = csv.writer(open_out, delimiter=',')
        file_o_csv.writerow(output)
  print(f'      {item_num} / {item_seg_num} products scraped')
  sleep(random.uniform(1, 3))
  pass

main_response = requests.get(main_url, headers = headers)
main_soup = BeautifulSoup(main_response.content, 'html.parser')

main_products_num = int(main_soup.find(class_ = 's-desktop-toolbar').text.split('results')[0].strip().split(' ')[-1].replace(',', ''))
print(f'\nThere are over {main_products_num} products.')

item_num = 0
low_price = 15
high_price = 20
price_interval = 2

if(main_products_num > 9600):
  while(True):
    print(f'\n***** low_{(str(low_price) if low_price is not None else "")} - high_{str(high_price) if high_price is not None else ""} *****')
    scrape_page(f'&low-price={(str(low_price) if low_price is not None else "")}&high-price={(str(high_price) if high_price is not None else "")}')
    
    if high_price == None:
      break
    
    low_price = high_price
    high_price = round(high_price + price_interval, 1)
    
    if high_price >= 80 and high_price < 150:
      price_interval = 1
      if int(high_price % 10) == 9:
        price_interval = 0.1
    elif high_price >= 150 and high_price < 330:
      price_interval = 10
    elif high_price > 330:
      high_price = None
else:
  scrape_page()
print('^^^^^ Finish ^^^^^')