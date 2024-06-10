import os
import pandas as pd

# Adjust the path to where your Excel files are stored
path = 'download'
output_file = '#PSREF_Title_jonas.xlsx'

# Define the columns to keep and the new column name
columns_to_keep = ['Model', 'Product', 'Display']
new_column_name = 'Title'
suffix = ' Replacement Screen'

# Find all Excel files in the directory
excel_files = [file for file in os.listdir(path) if file.endswith(('.xls', '.xlsx'))]

# Initialize an empty DataFrame to hold the merged data with new Title column
merged_df = pd.DataFrame()

for filename in excel_files:
    # Construct the full file path
    file_path = os.path.join(path, filename)
    
    # Read the entire sheet into a dataframe
    df = pd.read_excel(file_path)
    
    # Keep only the defined columns
    subset_df = df[columns_to_keep]
    
    # Remove commas, merge columns and add suffix
    subset_df[new_column_name] = subset_df.apply(
        lambda row: ' '.join(row.dropna().astype(str).str.replace(',', '')) + suffix, axis=1
    )
    
    # Append the processed data to the merged DataFrame
    merged_df = merged_df._append(subset_df[[new_column_name]], ignore_index=True)

# Drop duplicate titles from the merged DataFrame
merged_df.drop_duplicates(subset=[new_column_name], inplace=True)

# Write the resulting DataFrame to the output Excel file
merged_df.to_excel(output_file, index=False)
print(f"All Excel files have been merged into {output_file} with unique 'Title' column.")