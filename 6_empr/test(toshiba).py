from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests, csv
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ref_url = "https://store.emprgroup.com.au/p-392930-p000606020.aspx"
# while 1:
#     driver.get(ref_url)
#     els = driver.find_elements(By.CSS_SELECTOR, 'td.text-center')
#     print(len(els))
#     if len(els) > 0:
#         break
# product_compatible_model = []
# for eln in els:
#     compatible_model = eln.text.replace('  ', '')
#     if compatible_model == '':
#         break
#     product_compatible_model.append(eln.text)
# product_compatible_model = ','.join(product_compatible_model)
# print("Compatible Model: ", product_compatible_model)

print("DISPLAY")
url = "https://store.emprgroup.com.au/ToshibaParts.aspx?Name=DISPLAY"
base_url = '/'.join(url.split('/')[:-1])

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


page_num = soup.find_all(class_="page-number")
if len(page_num):
    page_num = page_num[-1].text
    print("Page Number: ", page_num)
    
    for i in range(1, int(page_num)+1):
        print(f"{i}Page")
        if i == 1:
            url_toshiba = url
            soup = soup
        else:
            url_toshiba = url + f"&pagenum={i}"
            response = requests.get(url_toshiba)
            soup = BeautifulSoup(response.content, 'html.parser')
            
        contents = soup.find_all(class_="product-heading")
            
        print(len(contents))
        if len(contents):
            for content in contents:
                list_all = []
                ref_url = content.findChild().get('href')
                ref_url = base_url + ref_url
                print("ref_url: ", ref_url)
                list_all.append(ref_url)
                response1 = requests.get(ref_url)
                soup1 = BeautifulSoup(response1.content, 'html.parser')
                try:
                    description = soup1.find(class_='product-description-wrap1')
                    product_description = description.text
                    product_description = product_description.replace('  ', '')
                    product_description = product_description.replace('\n', '')
                    if not('lcd' in product_description.lower() or 'panel' in product_description.lower() or 'led' in product_description.lower() or 'monitor' in product_description.lower() or 'display' in product_description.lower() or 'dsply' in product_description.lower()):
                        print('Keyword matching error!')
                        continue
                    print('Description: ', product_description)
                except:
                    product_description = ''
                    pass
                try:
                    product_part_number = description.find_next_sibling().text
                    product_part_number = product_part_number.replace('  ', '')
                    product_part_number = product_part_number.replace('\n', '')
                    product_part_number = product_part_number.replace('Part Number: ', '')
                    print('Part Number:', product_part_number)
                except:
                    product_part_number = ''
                    pass
                try:
                    product_availability = soup1.find_all(class_='colr')[0].text
                    product_availability = product_availability.replace('  ', '')
                    product_availability = product_availability.replace('\n', '')
                    print('Availability: ', product_availability)
                except:
                    product_availability = ''
                    pass
                try:
                    product_warranty = soup1.find_all(class_='colr')[1].text
                    product_warranty = product_warranty.replace("  ", "")
                    product_warranty = product_warranty.replace("\n", "")
                    product_warranty = product_warranty.replace("Warranty: ", "")
                    print("Warranty: ", product_warranty)
                except:
                    product_warranty = ''
                    pass
                try:
                    product_price = soup1.find(class_='product-price-large').text
                    product_price = product_price.replace("  ", "")
                    product_price = product_price.replace("\n", "")
                    print("Price: ", product_price)
                except:
                    product_price = ''
                    pass
                try:
                    while 1:
                        driver.get(ref_url)
                        els = driver.find_elements(By.CSS_SELECTOR, 'td.text-center')
                        print(len(els))
                        if len(els) > 0:
                            break
                    product_compatible_model = []
                    for eln in els:
                        compatible_model = eln.text.replace('  ', '')
                        if compatible_model == '':
                            break
                        product_compatible_model.append(eln.text)
                    product_compatible_model = ','.join(product_compatible_model)
                    print("Compatible Model: ", product_compatible_model)
                except:
                    product_compatible_model = ''
                    pass
                
                product_title = ''
                list_all.append(product_title)
                list_all.append(product_description)
                list_all.append(product_part_number)
                list_all.append(product_availability)
                list_all.append(product_warranty)
                list_all.append(product_price)
                product_compatible_part = ''
                list_all.append(product_compatible_part)
                list_all.append(product_compatible_model)
                
                open_out = open('toshiba.csv','a',newline="", encoding='utf-8')
                file_o_csv = csv.writer(open_out, delimiter=',')
                file_o_csv.writerow(list_all)
                open_out.close()
                print("---------------------------------")
        print("================================")

