import csv

with open('#chromebookparts (tag) TEMPLATE BLISS PORTAL UPLOAD.csv', 'r', encoding='latin-1') as csv_file:
  csv_reader = csv.reader(csv_file)
  for row in csv_reader:
    price_list = []
    price = float(row[2].replace('$', '').strip())
    if price < 50.0:
      price = 50.0
    price_list.append(price)
    out = open('output_price.csv','a',newline="", encoding='latin-1')
    file_o_csv = csv.writer(out, delimiter=',')
    file_o_csv.writerow(price_list)
    out.close()