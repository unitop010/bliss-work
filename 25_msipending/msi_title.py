import pandas as pd

# Reading the CSV file
df = pd.read_csv('msipending stock.csv')

# Function to fix Title_1
def fix_title(title):
    # Remove prefix
    if 'SYS DISPLAY MODULE,' in title:
        title = title.split('SYS DISPLAY MODULE,', 1)[1]
    # Replace "," with " "
    title = title.replace(",", " ")
    # Replace "/ " with "\n"
    title = title.replace("/ ", "/")
    return title

# Apply the function to the Title_1 column
df['Title_1'] = df['Title_1'].apply(fix_title)

# Save the modified DataFrame to a new CSV file
df.to_csv('fixed_file.csv', index=False)
