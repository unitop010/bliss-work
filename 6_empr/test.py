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

url_hp = 'https://store.emprgroup.com.au/lenovo-laptop-screen.aspx'
base_url = '/'.join(url_hp.split('/')[:-1])

response = requests.get(url_hp)

soup = BeautifulSoup(response.content, 'html.parser')

contents = soup.find_all(class_='col-md-2 col-sm-4 col-xs-6')
print(len(contents))
if len(contents):
    for content in contents:
        ref_url1 = content.findChildren()[0].findChildren()[0].get('href')
        ref_url1 = base_url + ref_url1
        print("ref_url1:", ref_url1)
        response1 = requests.get(ref_url1)
        soup1 = BeautifulSoup(response1.content, 'html.parser')
        contents1 = soup1.find_all(class_='col-md-4 col-sm-4 col-xs-6')
        print(len(contents1))
        if len(contents1):
            for content1 in contents1:
                ref_url2 = content1.findChildren()[0].findChildren()[0].get('href')
                ref_url2 = base_url + ref_url2
                print("ref_url2:", ref_url2)
                response2 = requests.get(ref_url2)
                soup2 = BeautifulSoup(response2.content, 'html.parser')
                contents2 = soup2.find_all(class_='col-md-4 col-sm-4 col-xs-6')
                print(len(contents2))
                print("--------------------------------------")
                if len(contents2):
                    for content2 in contents2:
                        ref_url3 = content2.findChildren()[0].findChildren()[0].get('href')
                        ref_url3 = base_url + ref_url3
                        print("ref_url3:", ref_url3)
                        response3 = requests.get(ref_url3)
                        soup3 = BeautifulSoup(response3.content, 'html.parser')
                        contents3 = soup3.find_all(class_='col-lg-9 col-md-9')
                        print(len(contents3))
                        print("--------------------------------------")
                        if len(contents3):
                            for content3 in contents3[1:]:
                                list_all = []
                                ref_url4 = content3.findChildren()[0].findChildren()[0].get('href')
                                ref_url4 = base_url + ref_url4
                                print("ref_url4:", ref_url4)
                                list_all.append(ref_url4)
                                
                                response4 = requests.get(ref_url4)
                                soup4 = BeautifulSoup(response4.content, 'html.parser')
                                try:
                                    description = soup4.find(class_='product-description-wrap1')
                                    product_description = description.text
                                    product_description = product_description.replace('  ', '')
                                    product_description = product_description.replace('\n', '')
                                    if not('LCD' in product_description or 'PANEL' in product_description or 'LED' in product_description or 'MONITOR' in product_description or 'DISPLAY' in product_description or 'DSPLY' in product_description):
                                        print('Keyword matching error!')
                                        continue
                                    print('Description: ', product_description)
                                except:
                                    product_description = ''
                                    pass
                                try:
                                    product_title = soup4.find(class_='flex-center-vertical-align1').text
                                    product_title = product_title.replace('  ', '')
                                    product_title = product_title.replace('\n', '')
                                    product_title = product_title.replace(' - View Certificate', '')
                                    print('Title: ', product_title)
                                except:
                                    product_title = ''
                                    pass
                                try:
                                    product_part_number = description.find_next_sibling().text
                                    product_part_number = product_part_number.replace('  ', '')
                                    product_part_number = product_part_number.replace('\n', '')
                                    product_part_number = product_part_number.replace('Part Number:', '')
                                    print('Part Number:', product_part_number)
                                except:
                                    product_part_number = ''
                                    pass
                                try:
                                    product_availability = soup4.find_all(class_='colr')[0].text
                                    product_availability = product_availability.replace('  ', '')
                                    product_availability = product_availability.replace('\n', '')
                                    print('Availability: ', product_availability)
                                except:
                                    product_availability = ''
                                    pass
                                try:
                                    product_warranty = soup4.find_all(class_='colr')[1].text
                                    product_warranty = product_warranty.replace("  ", "")
                                    product_warranty = product_warranty.replace("\n", "")
                                    product_warranty = product_warranty.replace("Warranty: ", "")
                                    print("Warranty: ", product_warranty)
                                except:
                                    product_warranty = ''
                                    pass
                                try:
                                    product_price = soup4.find(class_='product-price-large').text
                                    product_price = product_price.replace("  ", "")
                                    product_price = product_price.replace("\n", "")
                                    print("Price: ", product_price)
                                except:
                                    product_price = ''
                                    pass
                                try:
                                    product_compatible_part = soup4.find(class_='product-related-parts').text
                                    product_compatible_part = product_compatible_part.replace("  ", "")
                                    product_compatible_part = product_compatible_part.replace("\n", "")
                                    product_compatible_part = product_compatible_part.replace("Compatible Part: ", "")
                                    print("Compatible Part: ", product_compatible_part)
                                except:
                                    product_compatible_part = ''
                                    pass
                                try:
                                    driver.get(ref_url4)
                                    els = driver.find_elements(By.CLASS_NAME, 'col-lg-6')
                                    print(len(els))
                                    product_compatible_model = []
                                    for eln in els[1:]:
                                        compatible_model = eln.text.replace('  ', '')
                                        if compatible_model == '':
                                            break
                                        product_compatible_model.append(eln.text)
                                    product_compatible_model = ','.join(product_compatible_model)
                                    print("Compatible Model: ", product_compatible_model)
                                except:
                                    product_compatible_model = ''
                                    pass
                                list_all.append(product_title)
                                list_all.append(product_description)
                                list_all.append(product_part_number)
                                list_all.append(product_availability)
                                list_all.append(product_warranty)
                                list_all.append(product_price)
                                list_all.append(product_compatible_part)
                                list_all.append(product_compatible_model)
                                
                                open_out = open('new.csv','a',newline="", encoding='utf-8')
                                file_o_csv = csv.writer(open_out, delimiter=',')
                                file_o_csv.writerow(list_all)
                                open_out.close()
                        else:
                            print("No item.")
                        print("*****************************************")
                else:
                    print("No item.")
                print("--------------------------------------")
        else:
            print("No item.")
        print("==========================================")