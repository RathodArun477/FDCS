import pandas as pd
import ast
import os

os.makedirs("DataSets_Loaded", exist_ok=True)

COLUMN_MAP = {
    "Country": ["country", "area", "country name", "nation", "territory"],
    "ISO3": ["iso3", "iso_code", "iso"],
    "Temperature": ["temperature", "temp", "avg_temp", "average temperature", "mean temp"],
    "Element": ["element", "measurement", "type"],
    "Crop": ["crop", "crop name", "item"],
    "Value": ["value", "yield", "amount", "production", "quantity"],
    "RecipeName": ["recipe name", "dish", "meal"],
    "Ingredients": ["ingredients", "ingredient list", "components"]
}

COUNTRY_NORMALIZATION = {
    "china,mainland": "China",
    "usa": "United States",
    "u.s.a": "United States",
    "uk": "United Kingdom",
    "russia": "Russian Federation",
    "uae": "United Arab Emirates"
}

CUISINE_TO_COUNTRY = {
    "korean": "South Korea",
    "italian": "Italy",
    "indian": "India",
    "thai": "Thailand",
    "french": "France",
    "mexican": "Mexico",
    "greek": "Greece",
    "swedish": "Sweden",
    "ethiopian": "Ethiopia",
    "nigerian": "Nigeria",
    "peruvian": "Peru",
    "argentinian": "Argentina",
    "australian": "Australia",
    "polynesian": "Polynesia",
    "japanese": "Japan",
    "vietnamese": "Vietnam",
    "spanish": "Spain",
    "moroccan": "Morocco",
    "brazilian": "Brazil",
    "american": "United States",
    "jamaican": "Jamaica",
    "lebanese": "Lebanon",
    "irish": "Ireland",
    "chinese": "China"
}

def find_column(df, options):
    df_cols = [col.lower().strip() for col in df.columns]
    for opt in options:
        opt = opt.lower().strip()
        if opt in df_cols:
            return df.columns[df_cols.index(opt)]
    return None

def fix_list(x):
    if pd.isna(x):
        return []
    try:
        return ast.literal_eval(x)
    except:
        return []

countries = pd.read_csv("DataSets_Raw/Climate_1.csv")

country_col = find_column(countries, COLUMN_MAP["Country"])
iso3_col = find_column(countries, COLUMN_MAP["ISO3"])
temp_col = find_column(countries, COLUMN_MAP["Temperature"])

required = [country_col, iso3_col, temp_col]
if None in required:
    raise ValueError("Missing required columns in Climate_1.csv")

countries_clean = countries[[country_col, iso3_col, temp_col]].copy()
countries_clean.columns = ["Country", "ISO3", "Temperature"]

countries_clean["Country"] = (
    countries_clean["Country"].astype(str).str.lower().str.strip()
    .replace(COUNTRY_NORMALIZATION)
    .str.title()
)

countries_clean.to_csv("DataSets_Loaded/countries.csv", index=False)

crops = pd.read_csv("DataSets_Raw/Crops_1.csv")

country_col = find_column(crops, COLUMN_MAP["Country"])
crop_col = find_column(crops, COLUMN_MAP["Crop"])
value_col = find_column(crops, COLUMN_MAP["Value"])
element_col = find_column(crops, COLUMN_MAP["Element"])

required = [country_col, crop_col, value_col, element_col]
if None in required:
    raise ValueError("Missing required columns in Crops_1.csv")

crops_clean = crops[[country_col, crop_col, value_col, element_col]].copy()
crops_clean.columns = ["Country", "Crop", "Value", "Element"]

crops_clean["Country"] = (
    crops_clean["Country"].astype(str).str.lower().str.strip()
    .replace(COUNTRY_NORMALIZATION)
    .str.title()
)

crops_clean["Crop"] = crops_clean["Crop"].astype(str).str.lower().str.strip()
crops_clean["Element"] = crops_clean["Element"].astype(str).str.lower().str.strip()

crops_clean["Value"] = pd.to_numeric(crops_clean["Value"], errors="coerce")
crops_clean = crops_clean[crops_clean["Element"] == "production"]
crops_clean.rename(columns={"Value": "Production"}, inplace=True)

crops_country = crops_clean.groupby("Country", as_index=False)["Production"].sum()
crops_country["Production"] = crops_country["Production"].round(0).astype("Int64")

crops_clean.to_csv("DataSets_Loaded/crops.csv", index=False)
crops_country.to_csv("DataSets_Loaded/crops_country.csv", index=False)

recipes = pd.read_csv("DataSets_Raw/Recipes.csv")

recipes_clean = recipes.rename(columns={
    "RECIPE NAME": "Recipe Name",
    "cuisine": "Cuisine",
    "ingredients": "Ingredients",
    "cooking_time_minutes": "CookTime",
    "prep_time_minutes": "PrepTime",
    "servings": "Servings",
    "calories_per_serving": "CaloriesPerServing",
    "dietary_restrictions": "Dietary"
})

recipes_clean["Recipe Name"] = recipes_clean["Recipe Name"].astype(str).str.strip()
recipes_clean["CuisineLower"] = recipes_clean["Cuisine"].astype(str).str.lower().str.strip()

recipes_clean["Country"] = (
    recipes_clean["CuisineLower"]
    .map(CUISINE_TO_COUNTRY)
    .fillna("Unknown")
)

recipes_clean["Ingredients"] = recipes_clean["Ingredients"].apply(fix_list)
recipes_clean["Ingredients"] = recipes_clean["Ingredients"].apply(
    lambda lst: [i.lower().strip() for i in lst if isinstance(i, str)]
)

recipes_clean["Dietary"] = recipes_clean["Dietary"].apply(fix_list)
recipes_clean["Dietary"] = recipes_clean["Dietary"].apply(
    lambda lst: [d.lower().strip() for d in lst if isinstance(d, str)]
)

for col in ["CookTime", "PrepTime", "Servings", "CaloriesPerServing"]:
    recipes_clean[col] = pd.to_numeric(recipes_clean[col], errors="coerce")

recipes_clean.drop(columns=["CuisineLower"], inplace=True)
recipes_clean.to_csv("DataSets_Loaded/recipes.csv", index=False)

recipes_country = recipes_clean.groupby("Country", dropna=False).agg(
    Total_Recipes=("Recipe Name", "count"),
    Avg_Calories=("CaloriesPerServing", "mean"),
    Avg_CookTime=("CookTime", "mean"),
    Avg_PrepTime=("PrepTime", "mean")
).reset_index()

recipes_country["Avg_Calories"] = recipes_country["Avg_Calories"].round(2)
recipes_country["Avg_CookTime"] = recipes_country["Avg_CookTime"].round(1)
recipes_country["Avg_PrepTime"] = recipes_country["Avg_PrepTime"].round(1)


recipes_country.to_csv("DataSets_Loaded/recipes_country.csv", index=False)
