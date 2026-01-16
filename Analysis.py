import pandas as pd

df = pd.read_csv("DataSets_Loaded/countries.csv")

df.columns = df.columns.str.strip().str.lower()

country = input("Enter country name: ").strip().lower()

result = df[df['country'].str.lower() == country]

if result.empty:
    print("Country not found")
else:
    print("Climate:", result.iloc[0]['Temperature'])
