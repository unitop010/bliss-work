import csv

with open('system761.csv', 'r', encoding='latin-1') as csv_file:
  csv_reader = csv.reader(csv_file)
  for row in csv_reader:
    title = 'System76 '  + row[0].split('(')[0].strip() + ' ' + row[2] + ' ' + row[1].replace(' LCD', '').replace(' OLED', '') + ' Replacement Laptop LCD Panel'
    row.append(title)
    # print(title)
    # print(row)
    
    out = open('output.csv','a',newline="", encoding='latin-1')
    file_o_csv = csv.writer(out, delimiter=',')
    file_o_csv.writerow(row)
    out.close()