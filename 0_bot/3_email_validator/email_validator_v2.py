from verify_email import verify_email
from datetime import datetime
import csv
import multiprocessing
import os
import math

def verify_email_address(email):
    result = verify_email(email)
    return email if result else None

def process_emails(emails, email_tag, save_separate_files, emails_per_file, num_chunks):
    invalid_num = 0
    output_file_prefix = f'{email_tag}_email_{datetime.now().strftime("%Y-%m-%d")}'
    output_file_name = output_file_prefix

    current_file_num = 1
    current_emails = 0

    for email in emails:
        email = email.strip()
        valid_email = verify_email_address(email)
        
        if valid_email:
            first_name, last_name = valid_email.split('@')
            email_output = [valid_email, email_tag, 'Subscribed', first_name, last_name]
            
            if save_separate_files and current_emails >= emails_per_file // num_chunks:
                output_file_name = f'{output_file_prefix}_{current_file_num}'
                current_file_num += 1
                current_emails = 0
            
            with open(f'{output_file_name}.csv','a',newline="", encoding='utf-8') as open_out:
                file_o_csv = csv.writer(open_out, delimiter=',')
                file_o_csv.writerow(email_output)
                current_emails += 1
        else:
            invalid_num += 1
            print(f"Invalid email address '{email}'.")
    
    return invalid_num

def main():
    email_tag = input("Enter the email tag: ")

    save_separate_files = input("Do you want to save output into several files? (y/n): ").lower().strip() == 'y'
    emails_per_file = None
    if save_separate_files:
        emails_per_file = int(input("Enter the number of emails per file: "))
    
    with open('sws-test.csv', 'r+', encoding='utf-8') as file:
        emails = file.readlines()

    num_cores = multiprocessing.cpu_count()
    max_processes = 60  # Maximum number of processes supported in Windows
    num_chunks = min(num_cores * int(round(math.sqrt(num_cores))), max_processes)
    print(f"Using {num_chunks} processes.")
    
    email_chunks = [emails[i:i + len(emails) // num_chunks] for i in range(0, len(emails), len(emails) // num_chunks)]

    pool = multiprocessing.Pool(processes=num_chunks)
    results = [pool.apply_async(process_emails, args=(chunk, email_tag, save_separate_files, emails_per_file, num_chunks)) for chunk in email_chunks]
    pool.close()
    pool.join()

    invalid_num = sum(result.get() for result in results)
    total_emails = len(emails)
    valid_count = total_emails - invalid_num
    valid_rate = round((valid_count / total_emails) * 100, 2)
    
    print(f"----- All emails processed. -----\n Total: {total_emails}\n Valid: {valid_count}\n Invalid: {invalid_num}\n Valid Rate: {valid_rate}%")

if __name__ == "__main__":
    main()
