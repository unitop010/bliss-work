import csv
import re

# Define the path to your CSV file
csv_file_path = 'orders.csv'
output_file = 'verified_output.csv'

# Enhanced regex pattern to match various valid phone numbers
phone_number_pattern = re.compile(
    r'''
    (?:
        \(?\+?[0-9]{1,4}\)?[-.\s/]?
        (?:\(?[0-9]{1,3}\)?[-.\s/]?)+[0-9]+[-.\s/]?[0-9]+  # matches international patterns with country codes
    ) |
    (?:
        \(?\d{3}\)?[-.\s/]?\d{3}[-.\s/]?\d{4}  # matches patterns like (123) 456 7890, 123-456-7890, 123.456.7890
    ) |
    (?:
        \d{10}  # matches plain 10 digit numbers, e.g., 1234567890
    )
    ''', 
    re.VERBOSE
)

# Validate if the number is reasonable as a phone number
def is_valid_phone_number(number):
    number_digits = re.sub(r'\D', '', number)
    return 10 <= len(number_digits) <= 15 and not number.lstrip().startswith('-')  # No negative numbers and proper length

def extract_phone_numbers_from_csv(input_file, output_file):
    try:
        with open(input_file, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames + ['Phone Number']

            with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()

                for row in reader:
                    phone_number = None
                    numbers = [row.get('Customer', ''), row.get('Billing', ''), row.get('Shipping', '')]

                    for cell in numbers:
                        # Find matches and strip leading/trailing whitespace from each match
                        matches = [match.strip() for match in phone_number_pattern.findall(cell) if match.strip()]
                        valid_matches = [match for match in matches if is_valid_phone_number(match)]
                        if valid_matches:
                            phone_number = ', '.join(valid_matches)
                            break
                    
                    row['Phone Number'] = phone_number
                    writer.writerow(row)

    except FileNotFoundError:
        print(f"File not found: {input_file}")

extract_phone_numbers_from_csv(csv_file_path, output_file)
