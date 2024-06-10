import pandas as pd
import os
from datetime import datetime

# Path to the directory where all CSV files are stored
directory_path = 'output_2024-05-28'

# Get a list of all CSV filenames in the directory
csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

print(f"Found {len(csv_files)} CSV files in the directory '{directory_path}'.")

# Create a list to hold dataframes
dataframes_list = []

# Loop through all csv files, read them into dataframes with no headers, and append to list
for csv_file in csv_files:
    file_path = os.path.join(directory_path, csv_file)
    df = pd.read_csv(file_path, header=None)  # Read without headers
    dataframes_list.append(df)

# Concatenate all the dataframes in the list
merged_df = pd.concat(dataframes_list, ignore_index=True)

# Define column names if you know the structure of your CSV files
merged_df.columns = ['URL', 'Title', 'Price']

# Save the merged dataframe into a new CSV file with a timestamp
output_file_name = f'#amazon_Jonas_{datetime.now().strftime("%Y-%m-%d")}.csv'
merged_df.to_csv(output_file_name, index=False, header=False, encoding='utf-8-sig')  # Save without headers

print(f"All CSV files have been merged into {output_file_name}")
