import pandas as pd
import os

csv_file_date = '2024-05-29'
if not os.path.exists(csv_file_date):
  os.makedirs(csv_file_date)

df = pd.read_csv(f'#amazon_Jonas_{csv_file_date}.csv')

# Split the DataFrame into smaller DataFrames with 100 rows each
dfs = [df[i:i+10000] for i in range(0, len(df), 10000)]

for i, smaller_df in enumerate(dfs):
  smaller_df.to_csv(f'{csv_file_date}/#amazon_Jonas_{csv_file_date}_{i + 1}.csv', index=False)