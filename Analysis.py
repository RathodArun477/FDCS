import pandas as pd

df_temp=pd.read_csv("/content/drive/MyDrive/Major Project drive/countries.csv")
df_crop=pd.read_csv("/content/drive/MyDrive/Major Project drive/crops.csv")
df_totalproduction=pd.read_csv("/content/drive/MyDrive/Major Project drive/crops_country.csv")
df_recipe=pd.read_csv("/content/drive/MyDrive/Major Project drive/recipes.csv")
df_calories=pd.read_csv("/content/drive/MyDrive/Major Project drive/recipes_country.csv")

country_name=input("Enter country name: ").strip().lower()

df_temp['Country']=df_temp['Country'].str.strip().str.lower()
df_crop['Country']=df_crop['Country'].str.strip().str.lower()
df_totalproduction['Country']=df_totalproduction['Country'].str.strip().str.lower()
df_recipe['Country']=df_recipe['Country'].str.strip().str.lower()
df_calories['Country']=df_calories['Country'].str.strip().str.lower()

if country_name not in df_temp['Country'].values:
  print("Country not found. ")
  exit()

country_crops=df_crop[df_crop['Country']==country_name]

total_crop_production=country_crops['Production'].sum()

major_crops=(
    country_crops.groupby("Crop")["Production"].sum()
    .sort_values(ascending=False)
    .head(5)
)

country_recipes=df_recipe[df_recipe['Country']==country_name]

if country_recipes.empty:
  print("No recipes found for",country_name)

# country_recipes_calories=pd.merge(
#     country_recipes,
#     df_calories,
#     left_on=["Country","Recipe Name"],
#     right_on=["Country","Avg_Calories"],
#     how="left"
# )

# print("\n")

print(f"Total crop production in {country_name}: {total_crop_production}")
print("\n")
print("Major crops in",country_name,":")
print("\n")
print(major_crops)
print("\n")
print("Recipes in",country_name,":")
print("\n")
print(country_recipes[["Recipe Name","CaloriesPerServing"]])
print("\n")
# print("Calories in",country_name,":")
# print("\n")
# print(country_recipes_calories)
# print("\n")






