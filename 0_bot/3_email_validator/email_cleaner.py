import csv

# Define the input and output CSV file names
input_csv = 'SWS_email_2024-05-15.csv'
output_csv = 'SWS_email_2024-05-15_cleaned.csv'

def is_valid_email(email):
    return '@' in email

# Open the input CSV file for reading and the output CSV file for writing
with open(input_csv, mode='r', newline='') as infile, \
    open(output_csv, mode='w', newline='') as outfile:
    
    # Create a CSV reader and writer
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Iterate over each row in the input CSV
    for row in reader:
        # Check if the first element of the row is a valid email
        if row and is_valid_email(row[0]):
            # If it has an email, write the row to the output file
            writer.writerow(row)

print(f'Rows without valid emails have been removed. Check the file: {output_csv}')
