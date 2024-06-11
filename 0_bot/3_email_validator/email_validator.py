from verify_email import verify_email
from datetime import datetime
import csv
import multiprocessing
import os, math

def verify_email_address(email):
    result = verify_email(email)
    return email if result else None

def process_emails(emails, email_tag):
    invalid_num = 0
    
    output_file_name = f'{email_tag}_email_{datetime.now().strftime("%Y-%m-%d")}.csv'

    for email in emails:
        email = email.strip()
        valid_email = verify_email_address(email)
        
        if valid_email:
            first_name, last_name = valid_email.split('@')
            email_output = [valid_email, email_tag, 'Subscribed', first_name, last_name]
            
            open_out = open(output_file_name,'a',newline="", encoding='utf-8')
            file_o_csv = csv.writer(open_out, delimiter=',')
            file_o_csv.writerow(email_output)
            open_out.close()
        else:
            invalid_num += 1
            print(f"Invalid email address '{email}'.")
    
    return invalid_num

def main():
    email_tag = input("Enter the email tag: ")
    
    with open('test2.csv', 'r+', encoding='utf-8') as file:
        emails = file.readlines()

    # Split emails into chunks for parallel processing
    num_cores = multiprocessing.cpu_count()
    max_processes = 60  # Maximum number of processes supported in Windows
    num_chunks = min(num_cores * int(round(math.sqrt(num_cores))), max_processes)
    print(f"Using {num_chunks} processes.")
    num_chunks *= int(round(math.sqrt(num_chunks)))
    
    email_chunks = [emails[i:i + len(emails) // num_chunks] for i in range(0, len(emails), len(emails) // num_chunks)]

    pool = multiprocessing.Pool(processes=num_chunks)
    results = [pool.apply_async(process_emails, args=(chunk, email_tag)) for chunk in email_chunks]
    pool.close()
    pool.join()

    invalid_num = sum(result.get() for result in results)
    total_emails = len(emails)
    valid_count = total_emails - invalid_num
    valid_rate = round((valid_count / total_emails) * 100, 2)
    
    print(len(results))
    print(f"----- All emails processed. -----\n Total: {total_emails}\n Valid: {valid_count}\n Invalid: {invalid_num}\n Valid Rate: {valid_rate}%")

if __name__ == "__main__":
    main()
