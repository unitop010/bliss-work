import pandas as pd

# Define the path to your CSV file
csv_file_name = '#amazon_Jonas_2024-05-29'
csv_file_path = f'{csv_file_name}.csv'

# Read the CSV file without headers if there aren't any
df = pd.read_csv(csv_file_path, header=None)

# Specify the column index that you want to filter by
column_to_filter_by = 0  # assuming you want to filter by the first column

# List the keywords you want to check for removal
keywords_to_remove = ['Mobile','mobile', 'Phone', 'phone', 'Webcam', 'webcam', 'Touchpad', 'touchpad', 'Digitizer', 'digitizer', 'Protector', 'protector', 'Film', 'film', 'Frame', 'frame']

# Filter the dataframe to exclude rows containing any of the keywords
df_filtered = df[~df[column_to_filter_by].str.contains('|'.join(keywords_to_remove), na=False)]

# Save the filtered dataframe to a new CSV file with UTF-8-BOM encoding
output_csv_file_path = f'{csv_file_name}_cleaned.csv'
df_filtered.to_csv(output_csv_file_path, index=False, header=False, encoding='utf-8-sig')
