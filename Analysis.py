import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

countries_df = pd.read_csv("DataSets_Loaded/countries.csv")
crops_df = pd.read_csv("DataSets_Loaded/crops.csv")
crops_country_df = pd.read_csv("DataSets_Loaded/crops_country.csv")
recipes_df = pd.read_csv("DataSets_Loaded/recipes.csv")
recipes_country_df = pd.read_csv("DataSets_Loaded/recipes_country.csv")

country_name = input("Enter country name: ").strip().lower()

dataframes = [
    countries_df,
    crops_df,
    crops_country_df,
    recipes_df,
    recipes_country_df
]

for df in dataframes:
    df["Country"] = df["Country"].astype(str).str.strip().str.lower()

if country_name not in countries_df["Country"].values:
    print("Country not found in dataset")
    exit()

country_crops = crops_df[crops_df["Country"] == country_name]

production_array = np.array(country_crops["Production"])

total_crop_production = np.sum(production_array)
average_crop_production = np.mean(production_array)
max_crop_production = np.max(production_array)

major_crops = (
    country_crops
    .groupby("Crop")["Production"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

country_recipes = recipes_df[recipes_df["Country"] == country_name]

calorie_array = np.array(country_recipes["CaloriesPerServing"]) if not country_recipes.empty else np.array([])

total_calories = np.sum(calorie_array) if calorie_array.size > 0 else 0
average_calories = np.mean(calorie_array) if calorie_array.size > 0 else 0

print("\n==============================================")
print(f"Country: {country_name.title()}")
print("==============================================\n")

print(f"Total Crop Production      : {total_crop_production}")
print(f"Average Crop Production    : {average_crop_production:.2f}")
print(f"Highest Single Crop Output : {max_crop_production}\n")

print("Top 5 Major Crops:\n")
print(major_crops)

print("\n----------------------------------------------\n")

if country_recipes.empty:
    print("No recipes available for this country")
else:
    print("Traditional Recipes and Calories:\n")
    print(country_recipes[["Recipe Name", "CaloriesPerServing"]])
    print(f"\nTotal Calories (All Recipes) : {total_calories}")
    print(f"Average Calories per Recipe  : {average_calories:.2f}")

plt.figure(figsize=(10, 5))
major_crops.plot(kind="bar")
plt.title(f"Top 5 Crops Production in {country_name.title()}")
plt.xlabel("Crop")
plt.ylabel("Production")
plt.tight_layout()
plt.show()

if not country_recipes.empty:
    plt.figure(figsize=(10, 5))
    plt.bar(country_recipes["Recipe Name"], country_recipes["CaloriesPerServing"])
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Calories Distribution of Recipes in {country_name.title()}")
    plt.xlabel("Recipe")
    plt.ylabel("Calories per Serving")
    plt.tight_layout()
    plt.show()

print("\n==============================================")