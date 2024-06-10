import pandas as pd

# Load the Excel file into a DataFrame
df = pd.read_excel('3-20_output_somanyparts.xlsx')

# Replace 's\n' with '' (empty string) in Column G
# Assuming Column G is named 'G', replace 'G' with the actual column name if different
df.iloc[:, 6] = df.iloc[:, 6].astype(str).replace('s\n', '', regex=True)

# Save the modified DataFrame back to an Excel file
df.to_excel('3-20_output_somanyparts_s.xlsx', index=False)