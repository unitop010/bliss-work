import pandas as pd

# Define the file paths
input_file_path = "msipending stock_cleaned.csv"
output_file_path = "msipending stock_cleaned_cleaned.csv"

# Read in the CSV file
df = pd.read_csv(input_file_path)

# Remove duplicate rows based on the 'Title' column
df_unique = df.drop_duplicates(subset=['Title_1'])

# Save the cleaned data back to a new CSV file, without the index
df_unique.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print('-' * 5 + 'Finish' + '-' * 5)