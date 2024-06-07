import pandas as pd
df = pd.read_csv("output_impact.csv")
df = df.drop_duplicates()
df.to_csv("output_modified.csv", index=False)