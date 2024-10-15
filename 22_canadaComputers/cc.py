from bs4 import BeautifulSoup
import requests, csv
from urllib.parse import urljoin

url = 'https://www.canadacomputers.com/location.php'
print(f'~~~~~ URL: {url} ~~~~~')
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# html_content = str(soup.prettify)
# with open("webpage.html", "w", encoding="utf-8") as file:
#   file.write(html_content)
page_items = soup.findAll('div', class_='locwrapper')
for page_item in page_items:
  item_info = page_item.find(class_='order-1').findAll('a')
  item_url = urljoin(url, item_info[0]['href'])
  item_address = item_info[1].text.replace('\n','')
  item_phone = item_info[2].text
  item_email = item_info[3].text
  output = []
  output.append(item_url)
  output.append(item_address)
  output.append(item_phone)
  output.append(item_email)

  print(output)

  open_out = open('output_cc-20240919.csv','a',newline="", encoding='utf-8')
  file_o_csv = csv.writer(open_out, delimiter=',')
  file_o_csv.writerow(output)
  open_out.close()
  # else:
  #   continue
print('#' * 20 + 'Finish' + '#' * 20)