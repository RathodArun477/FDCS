import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR,"DataSets_Loaded")
def load_csv(file_name):
    path = os.path.join(DATA_DIR, file_name)

    if not os.path.exists(path):
        raise FileNotFoundError(f"{file_name} not found in DataSets_Loaded directory.")
    return pd.read_csv(path)

def strandize_country_names(df):
    if "Country" in df.columns:
        df["Country"] = df["Country"].astype(str).str.strip().str.lower()
    return df

def load_countries():
    df = load_csv("countries.csv")
    df = strandize_country_names(df)
    return df

def load_crops_country():
    df = load_csv("crops_country.csv")
    df = strandize_country_names(df)
    return df

def load_crops():
    df = load_csv("crops.csv")
    return df

def load_recipes():
    df = load_csv("recipes.csv")
    return df

def load_recipes_country():
    df = load_csv("recipes_country.csv")
    df = strandize_country_names(df)
    return df

def load_all():
    return {
        "countries" : load_countries(),
        "crops" : load_crops(),
        "crops_country" : load_crops_country(),
        "recipes" : load_recipes(),
        "recipes_country" : load_recipes_country()
    }