import requests
from bs4 import BeautifulSoup
from time import sleep
import csv

with open('brandUrls.csv', 'r+', encoding='utf-8') as urls:
    all_urls = urls.readlines()

def scrape_page(url):
    page_response = requests.get(url)
    page_soup = BeautifulSoup(page_response.content, 'html.parser')
    
    try:
        page_num = int(page_soup.find('nav.pagination').find_all('a')[-1].text)
    except:
        page_num = 1
    
    if page_num == 1:
        scrape_page_id(page_soup)
    else:
        for page_id in range(1, page_num + 1):
            page_id_response = requests.get(f'{url}?avia-element-paging={page_id}')
            page_id_soup = page_soup = BeautifulSoup(page_id_response.content, 'html.parser')
            scrape_page_id(page_id_soup)

def scrape_page_id(soup):
    products = soup.find('div.grid-sort-container').find_all('div.grid_entry')
    for product in products:
        product_url = product.find('header.entry-content-header').find('a')['href']
        product_title = product.find('header.entry-content-header').find('a').text
        
        output = [product_url, product_title]
        open_out = open('output.csv','a',newline="", encoding='utf-8-sig')
        file_o_csv = csv.writer(open_out, delimiter=',')
        file_o_csv.writerow(output)
        open_out.close()
        # scrape_product(product_url)
    sleep(0.5)

def scrape_product(url):
    
    pass

for url in all_urls:
    response = requests.get(url.strip())
    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        categories = soup.find('div.av-masonry-container').find_all('a')
        for category in categories:
            if 'LCD' in category.text or 'Touch' in category.text or 'Tablets' in category.text:
                category_url = category['href']
                scrape_page(category_url)
    except:
        scrape_page(url.strip())

# response = requests.get("https://www.ntcsupply.com/apple-parts/")

# with open("apple.html", "w", encoding="utf-8") as f:
#     f.write(response.text)