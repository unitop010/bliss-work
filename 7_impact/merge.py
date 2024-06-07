import os
import pandas as pd
# Specify the folder path where the Excel files are located
folder_path = '30'
# Get the list of excel files in the folder
file_list = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]
# Create an empty DataFrame to store the merged data
merged_data = pd.DataFrame()
# Iterate over each Excel file and append its contents to the merged_data DataFrame
for file in file_list:
    # Read the Excel file into a DataFrame, skipping the header row
    df = pd.read_excel(os.path.join(folder_path, file), header=None)
    # Append the contents of the current file to the merged_data DataFrame
    merged_data = merged_data.append(df, ignore_index=True)
# Save the merged_data DataFrame to a new Excel file
merged_data.to_excel('merged_output.xlsx', index=False)