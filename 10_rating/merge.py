import os
import pandas as pd

# Specify the folder path where the Excel files are located
folder_path = '10_rating'

# Get the list of excel files in the folder
file_list = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]

# Create an empty list to store the DataFrames
data_frames = []

# Iterate over each Excel file and append its contents to the data_frames list
for file in file_list:
    # Read the Excel file into a DataFrame, skipping the header row
    df = pd.read_excel(os.path.join(folder_path, file), header=None)
    # Check if the DataFrame is empty
    if df.empty:
        print(f"The file {file} is blank.")
    else:
        # Append the DataFrame to the data_frames list
        data_frames.append(df)

# Concatenate all non-blank DataFrames in the data_frames list into a single DataFrame
merged_data = pd.concat(data_frames, ignore_index=True)

# Save the merged_data DataFrame to a new Excel file
merged_data.to_excel('merged_output.xlsx', index=False)