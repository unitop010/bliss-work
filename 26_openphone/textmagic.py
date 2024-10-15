import csv

input_file = 'openphone.csv'
output_file = 'textMagic.csv'

with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
  reader = csv.DictReader(infile)
  rows = list(reader)

with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
  writer = csv.DictWriter(outfile)
  for index, row in enumerate(rows):
    row['TextMagic'] = f'{row['Fist Name']};{row['Last Name']};{row['Company']};{row['Phone Number']};{row['Email']}'
    writer.writerow(row)