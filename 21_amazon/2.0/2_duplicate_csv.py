import pandas as pd

# Define the file paths
input_file_path = "#amazon_Jonas_2024-05-29.csv"
output_file_path = "#amazon_Jonas_2024-05-29_cleaned.csv"

# Read in the CSV file
df = pd.read_csv(input_file_path)

# Remove duplicate rows based on the 'Title' column
df_unique = df.drop_duplicates(subset=['Title'])

# Save the cleaned data back to a new CSV file, without the index
df_unique.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print('-' * 5 + 'Finish' + '-' * 5)