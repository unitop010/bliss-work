import requests
from bs4 import BeautifulSoup

url = 'https://cell-doc.com/contact-us/'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

email_addresses = soup.find(class_ = 'main-content').find_all('a')

for email_address in email_addresses:
  if '@cell-doc.com' in email_address.text:
    print(email_address.text)

# with open('cell_doc.html', 'w') as f:
#   f.write(response.text)