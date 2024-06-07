from bs4 import BeautifulSoup
import requests, csv
import os

url = 'https://www.acerparts.ca/'
item_num = 0
process_log = []

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup.prettify)
# html_content = str(soup.prettify)
# with open("webpage.html", "w", encoding="utf-8") as file:
#   file.write(html_content)

with open('keywords.csv', 'r+', encoding='utf-8') as keywords:
  all_keywords = keywords.readlines()

for keyword in all_keywords:
  keyword_url = url.replace('\n', '') + 'shop/?s=' + keyword.replace('\n', '') + '&post_type=product&per_page=24'
  print(f'~~~~~ Keyword URL: {keyword_url} ~~~~~')
  response = requests.get(keyword_url)
  soup = BeautifulSoup(response.content, 'html.parser')
  
  # identify page number
  try:
    page_num = soup.find('nav', class_='woocommerce-pagination').find_all('li')
    page_num = page_num[-2].text
    print("Page Number:", page_num)
  except:
    print("!!!!! None keyword")
    continue
  
  for page_id in range(1, int(page_num) + 1):
    print(f'----- {page_id} page -----')
    page_url = url + f'shop/page/{page_id}/?s={keyword.replace('\n', '')}&post_type=product&per_page=24'
    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.content, 'html.parser')
    page_contents = page_soup.find_all(class_='product-wrapper')
    
    for page_content in page_contents:
      page_item_title = page_content.find('p').text.strip()
      if 'board' in page_item_title.lower() or 'circuit board' in page_item_title.lower() or 'battery' in page_item_title.lower() or 'keyboard' in page_item_title.lower() or 'desktop' in page_item_title.lower() or 'antenna' in page_item_title.lower() or 'wifi' in page_item_title.lower() or 'front cover' in page_item_title.lower() or 'back cover' in page_item_title.lower() or 'bottom base' in page_item_title.lower() or 'heatsink' in page_item_title.lower() or 'ac adapter' in page_item_title.lower() or 'ribbon' in page_item_title.lower() or 'cable' in page_item_title.lower() or 'bezel' in page_item_title.lower() or 'hinge' in page_item_title.lower() or 'cover' in page_item_title.lower() or 'screw' in page_item_title.lower():
        continue
      elif 'lcd' in page_item_title.lower() or 'led' in page_item_title.lower() or 'panel' in page_item_title.lower() or 'monitor' in page_item_title.lower() or 'display' in page_item_title.lower():
        output = []
        item_num += 1
        print('-' * 10, item_num, '-' * 10)
        page_item_url = page_content.find('a')['href']
        page_item_response = requests.get(page_item_url)
        page_item_soup = BeautifulSoup(page_item_response.content, 'html.parser')
        
        # title
        try:
          page_item_title_detailed = page_item_soup.find('div', class_='woocommerce-product-details__short-description').text.strip()
        except:
          page_item_title_detailed = ''
        
        # part number
        try:
          page_item_part = page_item_soup.find('h1', class_='product_title').text.strip()
        except:
          page_item_part = ''
        
        # price
        try:
          page_item_price = page_item_soup.find(class_='summary-inner').find_all(class_='woocommerce-Price-amount')[-1].text.strip()
        except:
          page_item_price = ''
        
        # description
        page_item_model1 = ''
        page_item_model2 = ''

        page_item_descriptions = page_item_soup.find('div', class_='wc-tab-inner').find_all('p')
        for page_item_description in page_item_descriptions:
          if page_item_description.text.startswith("Compatible Part Numbers"):
            page_item_model1 = page_item_description.text.split(':')[1].strip()
          elif page_item_description.text.startswith("Compatible Models"):
            page_item_model2 = page_item_description.text.split(':')[1].strip()
        
        output.append(page_item_url)
        output.append(page_item_title_detailed)
        output.append(page_item_price)
        output.append(page_item_part)
        output.append(page_item_model1)
        output.append(page_item_model2)
        
        print(output)
        
        open_out = open('output.csv','a',newline="", encoding='utf-8')
        file_o_csv = csv.writer(open_out, delimiter=',')
        file_o_csv.writerow(output)
        open_out.close()
print('*' * 20 + 'finish' + '*' * 20)