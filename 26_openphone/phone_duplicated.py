import csv

input_file = 'verified_output.csv'
output_file = 'duplicated_phone_removed.csv'

# Read the CSV data
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

# Track phone numbers and the latest row index with that phone number
phone_to_last_index = {}
for index, row in enumerate(rows):
    phone = row['Phone Number']
    if phone:  # Only consider non-empty phone numbers
        phone_to_last_index[phone] = index

# Filter rows, keeping only the last occurrence of each phone number
filtered_rows = []
for index, row in enumerate(rows):
    phone = row['Phone Number']
    if not phone or phone_to_last_index[phone] == index:
        filtered_rows.append(row)
    else:
        row['Phone Number'] = ''  # Remove the phone number from duplicates
    
# Write the updated rows to a new CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(filtered_rows)

print(f"Updated CSV written to {output_file}")
