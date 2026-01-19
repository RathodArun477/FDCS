import pandas as pd
import ast
import os

os.makedirs("DataSets_Loaded", exist_ok=True)

# ---------------- COLUMN MAP ----------------
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

# ---------------- HELPERS ----------------
def find_column(df, options):
    cols = [c.lower().strip() for c in df.columns]
    for opt in options:
        if opt.lower() in cols:
            return df.columns[cols.index(opt.lower())]
    return None

def fix_list(x):
    if pd.isna(x):
        return []
    try:
        return ast.literal_eval(x)
    except:
        return []

# ================= COUNTRIES =================
countries = pd.read_csv("DataSets_Raw/Climate_1.csv")

countries_clean = countries[["Country", "ISO3", "Temperature"]].copy()
countries_clean["Country"] = (
    countries_clean["Country"]
    .astype(str).str.lower().str.strip()
    .replace(COUNTRY_NORMALIZATION)
    .str.title()
)

countries_clean.to_csv("DataSets_Loaded/countries.csv", index=False)

# ================= CROPS =================
crops = pd.read_csv("DataSets_Raw/Crops_1.csv")

crops_clean = crops[["Area", "Item", "Element", "Value"]].copy()
crops_clean.columns = ["Country", "Crop", "Element", "Value"]

crops_clean["Country"] = (
    crops_clean["Country"]
    .astype(str).str.lower().str.strip()
    .replace(COUNTRY_NORMALIZATION)
    .str.title()
)

crops_clean["Crop"] = crops_clean["Crop"].astype(str).str.lower().str.strip()
crops_clean["Element"] = crops_clean["Element"].astype(str).str.lower().str.strip()
crops_clean["Value"] = pd.to_numeric(crops_clean["Value"], errors="coerce")

crops_clean = crops_clean[crops_clean["Element"] == "production"]
crops_clean.rename(columns={"Value": "Production"}, inplace=True)

crops_country = (
    crops_clean
    .groupby(["Country", "Crop"], as_index=False)["Production"]
    .sum()
)

crops_country["Production"] = crops_country["Production"].round(0).astype("Int64")

crops_clean.to_csv("DataSets_Loaded/crops.csv", index=False)
crops_country.to_csv("DataSets_Loaded/crops_country.csv", index=False)

# ================= RECIPES =================
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

recipes_country.to_csv("DataSets_Loaded/recipes_country.csv", index=False)
