import csv

input_file = 'duplicated_phone_removed.csv'
output_file = 'output.csv'

# Read the CSV data
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

# Track email addresses and the latest row index with that email address
email_to_last_index = {}
for index, row in enumerate(rows):
    email = row['Email']
    if email:  # Only consider non-empty email addresses
        email_to_last_index[email] = index

# Filter rows, keeping only the last occurrence of each email address
filtered_rows = []
for index, row in enumerate(rows):
    email = row['Email']
    if not email or email_to_last_index[email] == index:
        filtered_rows.append(row)
    else:
        row['Email'] = ''  # Remove the email address from duplicates

# Write the updated rows to a new CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(filtered_rows)

print(f"Updated CSV written to {output_file}")
