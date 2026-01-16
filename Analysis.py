import pandas as pd

print("Starting data cleaning...")
countries = pd.read_csv("DataSets_Raw/Climate_1.csv")

print("Raw country columns:")
print(countries.columns)

countries_clean = countries[["Country", "ISO3", "Temperature"]]
countries_clean["Country"] = countries_clean["Country"].str.strip()
countries_clean.to_csv("DataSets_Loaded/countries.csv", index=False)

print("countries.csv cleaned and saved")


crops = pd.read_csv("DataSets_Raw/Crop_Yield_1.csv")

print("Raw crop columns: ")
print(crops.columns)
crops_clean = crops[["Crop","Yield","Year"]]
