from bs4 import BeautifulSoup
import requests, csv
import os

url = 'https://www.impactcomputers.com/'
item_num = 0
process_log = []

with open('keywords.csv', 'r+', encoding='utf-8') as keywords:
  all_keywords = keywords.readlines()
  all_keywords.reverse()

def get_items(items):
  global item_num, log_indexes
  for index, item in enumerate(items):
    if log_indexes != [''] and log_indexes != []:
      index_value = int(log_indexes[0])
      if index < index_value:
        continue
      else:
        log_indexes.pop(0)
    elif os.path.isfile('C:\\Users\\Administrator\\Documents\\Work\\7_impact\\log.txt'):
      log_indexes = []
      log_in.close()
    item_url = url + item['href']
    print("Item URL:", item_url)
    item_response = requests.get(item_url)
    item_soup = BeautifulSoup(item_response.content, 'html.parser')
    process_log.append(index)
    try:
      item_contents = item_soup.find(class_='content-box-1').find_all('a')
      get_items(item_contents)
    except:
      print('=' * 20 + 'start' + '=' * 20)
      # save log info
      log_out = open('log.txt','w', encoding='utf-8')
      output_str = '-'.join(map(str, process_log))
      log_out.write(output_str)
      log_out.close()
      print(process_log)
      
      # identify page number
      try:
        page_num = item_soup.find(class_='pagination').find_all(class_="page")
        page_num = page_num[-3].text
      except:
        page_num = 1
      print("Page Number:", page_num)
      
      # start scraping
      for page_id in range(1, int(page_num) + 1):
        print(f'----- {page_id} Page')
        page_url = item_url + f'&page={page_id}'
        page_response = requests.get(page_url)
        page_soup = BeautifulSoup(page_response.content, 'html.parser')
        page_contents = page_soup.find_all(class_='product-module-item')
        for page_content in page_contents:
          page_item_title = page_content.find('h5').find('a').text.replace('  ', ' ')
          page_item_title_raw = ''.join(page_item_title.split(' - ')[1:])
          if 'board' in page_item_title_raw.lower() or 'circuit board' in page_item_title_raw.lower() or 'battery' in page_item_title_raw.lower() or 'keyboard' in page_item_title_raw.lower() or 'desktop' in page_item_title_raw.lower() or 'antenna' in page_item_title_raw.lower() or 'wifi' in page_item_title_raw.lower() or 'front cover' in page_item_title_raw.lower() or 'back cover' in page_item_title_raw.lower() or 'bottom base' in page_item_title_raw.lower() or 'heatsink' in page_item_title_raw.lower() or 'ac adapter' in page_item_title_raw.lower() or 'ribbon' in page_item_title_raw.lower() or 'cable' in page_item_title_raw.lower() or 'bezel' in page_item_title_raw.lower() or 'hinge' in page_item_title_raw.lower() or 'cover' in page_item_title_raw.lower() or 'screw' in page_item_title_raw.lower():
            continue
          elif 'lcd' in page_item_title_raw.lower() or 'led' in page_item_title_raw.lower() or 'panel' in page_item_title_raw.lower() or 'monitor' in page_item_title_raw.lower() or 'display' in page_item_title_raw.lower():
            for keyword_index, keyword in enumerate(all_keywords):
              # print(keyword_index)
              size = keyword.replace('\n', '')
              if size in page_item_title_raw.lower():
                output = []
                item_num = item_num + 1
                print('-' * 10, item_num, '-' * 10)
                page_item_url = page_content.find('h5').find('a')['href']
                page_item_response = requests.get(page_item_url)
                page_item_soup = BeautifulSoup(page_item_response.content, 'html.parser')
                
                # part number
                try:
                  page_item_part = page_item_soup.find(class_='manufacturer-list').find_all('li')[1].text.replace('Part Number:\n', '').strip()
                except:
                  page_item_part = ''
                  
                # price
                try:
                  page_item_price = page_item_soup.find(class_='price-new').text.split(':')[1]
                except:
                  page_item_price = ''
                  
                output.append(page_item_url)
                output.append(page_item_title)
                output.append(page_item_part)
                output.append(page_item_price)
                output.append('Replacement Laptop LCD LED Screen Display Monitor')
                
                print(output)
                
                open_out = open('output_impact.csv','a',newline="", encoding='utf-8')
                file_o_csv = csv.writer(open_out, delimiter=',')
                file_o_csv.writerow(output)
                open_out.close()
                break
              else:
                continue
          else:
            continue
      print('-' * 20 + 'end' + '-' * 20)
    process_log.pop()

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
contents = soup.find(class_='panel-body').find_all('a')
print(f'Brand Number: {len(contents)}')
if len(contents):
  for index, content in enumerate(contents):
    brand_url = content['href']
    print("*****Brand URL:", brand_url)
    
    # load log info
    if os.path.isfile('C:\\Users\\Administrator\\Documents\\Work\\7_impact\\log.txt'):
      with open('log.txt', 'r', encoding='utf-8') as log_in:
        if log_in:
          log_indexes = log_in.read().split('-')
        else:
          log_indexes = []
      if log_indexes != [''] and log_indexes != []:
        index_value = int(log_indexes[0])
        if index < index_value:
          continue
        elif index == index_value:
          log_indexes.pop(0)
        else:
          log_indexes = []
      else:
        log_in.close()
    else:
      log_indexes = []
    
    process_log.append(index)
    response1 = requests.get(brand_url)
    soup1 = BeautifulSoup(response1.content, 'html.parser')
    contents1 = soup1.find(class_='content-box-1').find_all('a')
    print(f'Content Number: {len(contents1)}')
    get_items(contents1)
    process_log.pop()
    print('^' * 20 + 'NEXT BRAND' + '^' * 20)
  print('#' * 20 + 'Finish' + '#' * 20)