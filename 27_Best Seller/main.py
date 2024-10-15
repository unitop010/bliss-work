import pandas as pd

# Load data from input.csv
df = pd.read_csv('input.csv')

# Replace NaN values with 0 in the sold column
df['sold'] = df['sold'].fillna(0)

# Convert sold column to integers
df['sold'] = df['sold'].astype(int)

# Sort the dataframe by gid and then by sold in descending order
df_sorted = df.sort_values(by=['gid', 'sold'], ascending=[True, False])

# Drop duplicates based on gid to keep only the most sold product in each group
most_sold_products = df_sorted.drop_duplicates(subset='gid', keep='first')

# Save the result to a new CSV file named output.csv
most_sold_products.to_csv('output.csv', index=False)

print(most_sold_products)
