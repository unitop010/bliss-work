import pandas as pd

df = pd.read_csv("output.csv", encoding='latin-1')
df = df.drop_duplicates()
df.to_csv("output_acerparts.csv", index=False)
print('-' * 5 + 'Finish' + '-' * 5)