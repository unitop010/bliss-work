import pandas as pd
# Read the Excel file
df = pd.read_excel("output_laptopmedia-9.xlsx")
# Remove duplicates based on all columns
df = df.drop_duplicates()
# Save the updated DataFrame to a new Excel file
df.to_excel("output_modified.xlsx", index=False)