import pandas as pd

file_path = "data_clean.csv"

df = pd.read_csv(file_path)

# id starts from 1
df.insert(0, "id", range(1, len(df) + 1))

df.to_csv(file_path, index=False)

print("ID added starting from 1")