from bs4 import BeautifulSoup
import requests, csv
import os

item_num = 0
process_log = []

with open('urls.csv', 'r+', encoding='utf-8') as urls:
  all_urls = urls.readlines()
with open('keywords.csv', 'r+', encoding='utf-8') as keywords:
  all_keywords = keywords.readlines()
  
for url_index, url in enumerate(all_urls):
  for keyword in all_keywords:
    keyword_url = url.replace('\n', '') + '/' + keyword.replace('\n', '') + '.html'
    print(f'~~~~~ Keyword URL: {keyword_url} ~~~~~')
    response = requests.get(keyword_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # identify page number
    try:
      page_num = soup.find('ul', id='page1').find_all('a')
      page_num = page_num[-2].text
      print("Page Number:", page_num)
    except:
      print("!!!!! None keyword")
      continue
    
    for page_id in range(1, int(page_num) + 1):
      print(f'----- {page_id} page -----')
      page_url = keyword_url + f'?=p{page_id}'
      page_response = requests.get(page_url)
      page_soup = BeautifulSoup(page_response.content, 'html.parser')
      page_contents = page_soup.find(id='choice_product').find('tbody').find_all('tr')
      
      for page_content in page_contents:
        page_item_desc = page_content.find('td', class_='descr').text.strip()
        # if 'motherboard' in page_item_desc.lower() or 'circuit board' in page_item_desc.lower() or 'battery' in page_item_desc.lower() or 'keyboard' in page_item_desc.lower() or 'desktop' in page_item_desc.lower() or 'antenna' in page_item_desc.lower() or 'wifi' in page_item_desc.lower() or 'front cover' in page_item_desc.lower() or 'back cover' in page_item_desc.lower() or 'bottom base' in page_item_desc.lower() or 'heatsink' in page_item_desc.lower() or 'ac adapter' in page_item_desc.lower() or 'ribbon' in page_item_desc.lower():
        #   continue
        # elif 'lcd' in page_item_desc.lower() or 'led' in page_item_desc.lower() or 'panel' in page_item_desc.lower() or 'monitor' in page_item_desc.lower() or 'display' in page_item_desc.lower():
        output = []
        item_num += 1
        print('-' * 10, item_num, '-' * 10)
        page_item_url = page_content.find('td', class_='search-eos').find('a')['href']
        # page_item_response = requests.get(page_item_url)
        # page_item_soup = BeautifulSoup(page_item_response.content, 'html.parser')
        
        # part number
        try:
          page_item_part = page_content.find('td', class_='search-eos').find('a').text.strip()
        except:
          page_item_part = ''
        
        # title
        if url_index == 0:
          page_item_title = "HP/HPE " + page_item_part
        elif url_index == 1:
          page_item_title = "DELL " + page_item_part
          
        # price
        try:
          page_item_price = page_content.find('td', class_='text-right').text.strip()
        except:
          page_item_price = ''
          
        output.append(page_item_url)
        output.append(page_item_title)
        output.append('Replacement Laptop LCD LED Screen Display Monitor')
        output.append(page_item_part)
        output.append(page_item_desc)
        output.append(page_item_price)
        
        print(output)
        
        open_out = open('output.csv','a',newline="", encoding='utf-8')
        file_o_csv = csv.writer(open_out, delimiter=',')
        file_o_csv.writerow(output)
        open_out.close()
        # else:
        #   continue
print('#' * 20 + 'Finish' + '#' * 20)