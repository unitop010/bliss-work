import pandas as pd

# Read the two Excel files into pandas DataFrames
df1 = pd.read_excel('link-less.xlsx')
df2 = pd.read_excel('link-all.xlsx')

# Find the difference between the two DataFrames
diff_df = pd.concat([df1, df2]).drop_duplicates(keep=False)

# Save the difference to a new Excel file
diff_df.to_excel('link-diff.xlsx', index=False)