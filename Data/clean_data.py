import pandas as pd
import os

csv_path = os.path.join(".", "Data", "raw_data.csv")
df = pd.read_csv(csv_path)


df ["suprafata"] = df ["suprafata"].str.replace(" ", "", regex=False)
df ["suprafata"] = df ["suprafata"].str.replace("m²", "", regex=False)
df ["pret"] = df ["pret"].str.replace(" ", "", regex=False)
df ["pret"] = df ["pret"].str.replace("€", "", regex=False)


df.to_csv('clean_data.csv', index=False, encoding='utf-8-sig')

    