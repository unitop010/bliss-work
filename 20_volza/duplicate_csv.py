import pandas as pd
df = pd.read_csv("output.csv")
df = df.drop_duplicates()
df.to_csv("output_volza.csv", index=False)
print('-' * 5 + 'Finish' + '-' * 5)