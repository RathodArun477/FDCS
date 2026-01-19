import pandas as pd
import numpy as np
from Data_Load import load_all
import re
from collections import Counter

def tokenize(text):
    return re.findall(r"[a-zA-Z]+",text.lower())

CROP_CATEGORIES = {

    # --- CEREALS / GRAINS ---
    "cereals": {
        "keywords": [
            "wheat","rice","maize","corn","barley","oats","rye",
            "sorghum","millet","triticale","buckwheat","fonio",
            "mixed grain","cereals"
        ],
        "temp_range": (10, 32)
    },

    # --- LEGUMES / PULSES ---
    "pulses": {
        "keywords": [
            "beans","peas","lentil","chick","cow pea","pigeon pea",
            "lupin","vetch","bambara","broad beans","horse beans"
        ],
        "temp_range": (15, 30)
    },

    # --- VEGETABLES (GENERAL + FRESH) ---
    "vegetables": {
        "keywords": [
            "cabbage","carrot","cauliflower","broccoli","tomato",
            "eggplant","aubergine","pumpkin","squash","gourd","okra",
            "spinach","lettuce","chicory","leeks","onions","shallots",
            "garlic","mushroom","truffle","string beans","green beans",
            "peas, green","other vegetables"
        ],
        "temp_range": (10, 30)
    },

    # --- ROOTS & TUBERS ---
    "roots_tubers": {
        "keywords": [
            "potato","cassava","yam","taro","sweet potato","yautia",
            "edible roots","tubers"
        ],
        "temp_range": (10, 30)
    },

    # --- TROPICAL FRUITS ---
    "tropical_fruits": {
        "keywords": [
            "banana","plantain","mango","guava","mangosteen",
            "papaya","pineapple","coconut","avocado",
            "dates","tropical fruits"
        ],
        "temp_range": (20, 35)
    },

    # --- TEMPERATE FRUITS ---
    "temperate_fruits": {
        "keywords": [
            "apple","pear","plum","peach","nectarine","apricot",
            "cherry","grape","kiwi","persimmon","quince",
            "blueberries","raspberries","cranberries","currants",
            "gooseberries"
        ],
        "temp_range": (5, 25)
    },

    # --- CITRUS FRUITS ---
    "citrus": {
        "keywords": [
            "orange","lemons","limes","tangerine","mandarin",
            "clementine","pomelos","grapefruits","citrus"
        ],
        "temp_range": (15, 30)
    },

    # --- MELONS ---
    "melons": {
        "keywords": [
            "watermelon","cantaloupe","melons"
        ],
        "temp_range": (20, 32)
    },

    # --- NUTS ---
    "nuts": {
        "keywords": [
            "almond","walnut","pistachio","hazelnut","chestnut",
            "cashew","brazil nut","kola nut","shea","karite","areca"
        ],
        "temp_range": (10, 30)
    },

    # --- OILSEEDS ---
    "oilseeds": {
        "keywords": [
            "soy","sunflower","sesame","groundnut","peanut","mustard",
            "safflower","linseed","rapeseed","colza","castor","melonseed",
            "shea","tung","oil palm"
        ],
        "temp_range": (15, 35)
    },

    # --- SPICES, HERBS, AROMATICS ---
    "spices": {
        "keywords": [
            "pepper","ginger","nutmeg","mace","cardamom","cinnamon",
            "clove","vanilla","mint","anise","coriander","cumin",
            "caraway","fennel","juniper","curry","spice"
        ],
        "temp_range": (20, 32)
    },

    # --- BEVERAGE CROPS ---
    "beverages": {
        "keywords": [
            "coffee","tea","cocoa","mate","hop cones"
        ],
        "temp_range": (15, 28)
    },

    # --- FIBRE CROPS ---
    "fibres": {
        "keywords": [
            "cotton","jute","hemp","flax","sisal","kenaf",
            "ramie","agave","abaca","manila hemp","coir"
        ],
        "temp_range": (15, 35)
    },

    # --- SWEETENERS ---
    "sugar_crops": {
        "keywords": [
            "sugar cane","sugar beet"
        ],
        "temp_range": (15, 35)
    },

    # --- OTHER CROPS ---
    "other": {
        "keywords": [
            "natural honey","beeswax","tobacco"
        ],
        "temp_range": (10, 30)
    },
    
    #--- BERRIES ---
    "berries": {
    "keywords": [
        "blueberries","raspberries","cranberries","currants",
        "gooseberries","berry"
    ],
    "temp_range":(5,20)
}
}

invalid_crops = [
    "cattle fat, unrendered",
    "edible offal of cattle, fresh, chilled or frozen",
    "edible offal of goat, fresh, chilled or frozen",
    "edible offal of sheep, fresh, chilled or frozen",
    "edible offals of camels and other camelids, fresh, chilled or frozen",
    "fat of camels",
    "game meat, fresh, chilled or frozen",
    "goat fat, unrendered",
    "meat of camels, fresh or chilled",
    "meat of cattle with the bone, fresh or chilled",
    "meat of chickens, fresh or chilled",
    "meat of goat, fresh or chilled",
    "meat of sheep, fresh or chilled",
    "raw hides and skins of cattle",
    "raw hides and skins of goats or kids",
    "raw hides and skins of sheep or lambs",
    "raw milk of camel",
    "raw milk of cattle",
    "raw milk of goats",
    "raw milk of sheep",
    "sheep fat, unrendered",
    "shorn wool, greasy, including fleece-washed shorn wool",
    "edible offal of pigs, fresh, chilled or frozen",
    "fat of pigs",
    "meat of pig with the bone, fresh or chilled",
    "meat of turkeys, fresh or chilled",
    "meat of asses, fresh or chilled",
    "meat of ducks, fresh or chilled",
    "meat of geese, fresh or chilled",
    "meat of mules, fresh or chilled",
    "other meat of mammals, fresh or chilled",
    "edible offals of horses and other equines, fresh, chilled or frozen",
    "horse meat, fresh or chilled",
    "meat of rabbits and hares, fresh or chilled",
    "meat of other domestic camelids, fresh or chilled",
    "meat of other domestic rodents, fresh or chilled",
    "raw milk of buffalo",
    "buffalo fat, unrendered",
    "edible offal of buffalo, fresh, chilled or frozen",
    "meat of buffalo, fresh or chilled",
    "raw hides and skins of buffaloes",
    "meat of pigeons and other birds n.e.c., fresh, chilled or frozen",
    "snails, fresh, chilled, frozen, dried, salted or in brine, except sea snails"
]

INVALID_CROPS_SET = set(c.lower() for c in invalid_crops)

BAD_TOKENS = {
    "meat","milk","fat","offal","hide","hides","skin","skins","wool","snail"
}

data = load_all()

countries_df = data["countries"]
crops_df = data["crops"]
crops_country_df = data["crops_country"]
recipes_df = data["recipes"]
recipes_country_df = data["recipes_country"]

all_crops = crops_df["Crop"].astype(str).str.lower().unique().tolist()

def classify_temp(temp_c):
    if temp_c > 25 and temp_c <=35:
        return "Tropical"
    elif temp_c > 15 and temp_c <=25:
        return "Subtropical"
    elif temp_c > 5 and temp_c <=15:
        return "Temperate"
    else:
        return "Cold"

CLIMATE_TO_CATEGORIES = {
    "Tropical": ["tropical_fruits", "oilseeds", "spices", "roots_tubers", "cereals", "melons"],
    "Subtropical": ["vegetables", "cereals", "pulses", "nuts", "oilseeds", "citrus"],
    "Temperate": ["temperate_fruits", "berries","cereals", "vegetables", "nuts"],
    "Cold": ["temperate_fruits", "cereals", "roots_tubers"]
}

def get_crop_category(crop_name):
    crop_tokens = set(tokenize(crop_name))

    for category, details in CROP_CATEGORIES.items():
        for keyword in details["keywords"]:
            keyword_tokens = set(tokenize(keyword))

            if keyword_tokens.issubset(crop_tokens):
                return category

    return "other"


def categorize_country(country):
    country = str(country).strip().lower()
    row = countries_df[
        countries_df["Country"].astype(str).str.lower() == country
    ]
    if row.empty:
        return None
    temp_val = row.iloc[0].get("Temperature", None)
    if pd.isna(temp_val):
        return None
    
    temp_c = float(temp_val)
    
    return classify_temp(temp_c)

def valid_crop(crop_name):
    if not crop_name:
        return False
    crop_name = str(crop_name).lower()
    if crop_name in INVALID_CROPS_SET:
        return False
    
    tokens = crop_name.replace(",","").split()
    if any(token in BAD_TOKENS for token in tokens):
        return False
    return True

def analyze_crop_climate(country):
    climate_type = categorize_country(country)
    if climate_type is None:
        return None
    
    if climate_type not in CLIMATE_TO_CATEGORIES:
        return None
    
    raw_crops = crops_country_df[
        crops_country_df["Country"].astype(str).str.lower() == country
    ]["Crop"].astype(str).tolist()
    
    categorized_crops = []
    suitable = []
    unusual = []

    for crop in raw_crops:
        if not valid_crop(crop):
            continue

        category = get_crop_category(crop)
        categorized_crops.append((crop, category))

        normalized = ingredients_to_crops([crop])  # ALWAYS returns list

        if category in CLIMATE_TO_CATEGORIES[climate_type]:
            suitable.extend(normalized)
        else:
            unusual.extend(normalized)

    return {
        "climate_type": climate_type,
        "suitable_crops": list(set(suitable)),
        "unusual_crops": list(set(unusual)),
        "categorized_crops": categorized_crops
    }


def recipe_to_ingredients(recipe_name):
    recipe_name = str(recipe_name).strip().lower()
    row = recipes_df[recipes_df["Recipe Name"].astype(str).str.lower() == recipe_name]
    if row.empty:
        return None
    
    ingredients = row.iloc[0]["Ingredients"]
    if pd.isna(ingredients):
        return []
    
    ingredients_list = [i.strip().lower() for i in ingredients.split(",")]
    return ingredients_list

def ingredients_to_crops(ingredients):
    if not ingredients:
        return []
    token_lists = [tokenize(ing) for ing in ingredients]
    tokens = {tok for tlist in token_lists for tok in tlist}
    
    possible_crops = [
        crop.lower() for crop in crops_df["Crop"].astype(str).tolist()
        if valid_crop(crop)
    ]
    
    matched = []
    
    for crop in possible_crops:
        crop_tokens = tokenize(crop)
        
        if any(tok in tokens for tok in crop_tokens):
            matched.append(crop)
            continue
        
        overlap_count = sum(1 for tok in crop_tokens if tok in tokens)
        if len(crop_tokens) > 0 and (overlap_count)/ len(crop_tokens) > 0.5:
            matched.append(crop)
            
    return list(set(matched))

def get_country_for_crops(crop_list):
    if not crop_list:
        return {}

    crop_to_countries = {}

    df = crops_country_df.copy()
    df["crop_tokens"] = df["Crop"].astype(str).str.lower().apply(tokenize)

    for crop in crop_list:
        c_tokens = set(tokenize(crop))

        matched_countries = df[
            df["crop_tokens"].apply(lambda toks: c_tokens.issubset(set(toks)))
        ]["Country"].astype(str).str.lower().tolist()

        crop_to_countries[crop] = matched_countries

    return crop_to_countries


def full_analyze_recipe(recipe_name):
    recipe_name = str(recipe_name).strip().lower()
    ingredients = recipe_to_ingredients(recipe_name)
    if ingredients is None:
        return {
            "recipe name":recipe_name,
            "ingredients":None,
            "crops":None,
            "countries_for_crops":None,
        }
    
    crops = ingredients_to_crops(ingredients)
    if crops is None or len(crops) == 0:
        crops = []
    countries_for_crops = get_country_for_crops(crops)
    if countries_for_crops is None:
        countries_for_crops = {}
    
    return {
        "recipe_name":recipe_name,
        "ingredients":ingredients,
        "crops":crops,
        "countries_for_crops":countries_for_crops,
    }

def country_to_recipe_and_crops(country):
    country = str(country).strip().lower()
    result = {
        "country" : country,
        "recipes": [],
        "ingredients" : [],
        "crops":[],
        "countries_for_crops":{},
        "local_crops" : [],
        "imported_crops":[]
    }
    country_recipe = recipes_df[recipes_df["Country"].astype(str).str.lower() == country]
    result["recipes"] = country_recipe["Recipe Name"].astype(str).tolist()
    
    all_ingredients = []
    for ing in country_recipe["Ingredients"].astype(str).tolist():
        ing = [i.strip().lower() for i in ing.split(",")]
        all_ingredients.extend(ing)
    result["ingredients"] = list(set(all_ingredients))
    
    crops_in_ingredients = ingredients_to_crops(result["ingredients"])
    result["crops"] = [c.lower() for c in (crops_in_ingredients or [])]
    
    result["countries_for_crops"] = get_country_for_crops(result["crops"])
    
    local_crops = crops_country_df[crops_country_df["Country"].astype(str).str.lower() == country]["Crop"].astype(str).str.lower().tolist()
    result["local_crops"] = [crop for crop in result["crops"] if crop in local_crops]
    
    imported = [crop for crop in result["crops"] if crop not in local_crops]
    result["imported_crops"] = imported
    return result


def analyze_crop_dependency(crops_used,local_crops,imported_crops):
    if not crops_used or len(crops_used) == 0:
        return {
            "total_crops_used":0,
            "local_crops_used":0,
            "imported_crops_used":0,
            "dominant_crops" : []
        }
    total_crops_used = len(set(crops_used))
    local_crops_used = len(set(local_crops))
    imported_crops_used = len(set(imported_crops))
    
    local_ratio = local_crops_used / total_crops_used if total_crops_used > 0 else 0.0
    imported_ratio = imported_crops_used / total_crops_used if total_crops_used > 0 else 0.0
    
    dominant_crops = [
        crop for crop, _ in Counter(crops_used).most_common(3)
    ]
    
    return {
        "total_crops_used": total_crops_used,
        "local_crops_used": local_crops_used,
        "imported_crops_used": imported_crops_used,
        "local_ratio": round(local_ratio, 3),
        "imported_ratio": round(imported_ratio, 3),
        "dominant_crops": [c.lower() for c in dominant_crops]
    }
 
def analyze_climate_alignment(suitable_crops, climate, crops_used):
    if not crops_used:
        return {
            "alignment_score": 0.0,
            "aligned_crops": [],
            "unaligned_crops": []
        }

    aligned = [crop for crop in crops_used if crop in suitable_crops]
    unaligned = [crop for crop in crops_used if crop not in suitable_crops]

    total = len(set(crops_used))
    score = len(set(aligned)) / total if total else 0

    return {
        "alignment_score": round(score, 3),
        "aligned_crops": aligned,
        "unaligned_crops": unaligned
    }

def generate_cultural_insights(country, climate, crop_dependency, climate_alignment):
    if climate is None:
        return "Climate data is unavailable for this country."

    local_ratio = crop_dependency.get("local_ratio", 0)
    imported_ratio = crop_dependency.get("imported_ratio", 0)

    dominant_crops = crop_dependency.get("dominant_crops", [])

    alignment_score = climate_alignment.get("alignment_score", 0)
    aligned_crops = climate_alignment.get("aligned_crops", [])
    misaligned_crops = climate_alignment.get("unaligned_crops", [])

    s1 = (
        f"{country.title()} has a {climate.lower()} climate, "
        f"which heavily influences the types of crops that thrive there."
    )

    s2 = (
        f"Its cuisine is built on {len(dominant_crops)} core crops, "
        f"with roughly {int(local_ratio * 100)}% coming from local agriculture "
        f"and about {int(imported_ratio * 100)}% relying on imports."
    )

    s3 = (
        f"Around {int(alignment_score * 100)}% of the crops used in national dishes "
        f"fit well with the country's natural climate conditions."
    )

    if alignment_score > 0.7 and local_ratio > 0.7:
        s4 = (
            f"This strong alignment signals a cuisine deeply rooted in the land — "
            f"a stable and traditional agricultural identity."
        )

    elif alignment_score < 0.3 and imported_ratio > 0.5:
        s4 = (
            f"The heavy reliance on imported crops shows a globally-influenced, "
            f"diverse food culture shaped by trade and external flavors."
        )

    else:
        s4 = (
            f"The mix of local and imported crops creates a dynamic culinary scene, "
            f"blending home-grown traditions with outside influences."
        )

    return " ".join([s1, s2, s3, s4])

def analyze_all_cuisine(country):
    country = str(country).strip().lower()

    result = {
        "country": country,
        "climate": None,
        "suitable_crops": [],
        "unusual_crops": [],
        "recipes": [],
        "ingredients_used": [],
        "crops_used_in_recipes": [],
        "local_crops": [],
        "imported_crops": [],
        "countries_for_crops": {},
        "crop_dependency": {},
        "climate_alignment": {},
        "analysis_summary": ""
    }

    climate_info = analyze_crop_climate(country)
    if climate_info:
        result["climate"] = climate_info["climate_type"]
        result["suitable_crops"] = climate_info["suitable_crops"]
        result["unusual_crops"] = climate_info["unusual_crops"]
    else:
        result["climate"] = None
        result["suitable_crops"] = []
        result["unusual_crops"] = []

    food_info = country_to_recipe_and_crops(country)

    result["recipes"] = food_info["recipes"]
    result["ingredients_used"] = food_info["ingredients"]
    result["crops_used_in_recipes"] = food_info["crops"]

    result["local_crops"] = food_info["local_crops"]
    result["imported_crops"] = food_info["imported_crops"]
    result["countries_for_crops"] = food_info["countries_for_crops"]

    crop_dependency = analyze_crop_dependency(
        result["crops_used_in_recipes"],
        result["local_crops"],
        result["imported_crops"]
    )
    result["crop_dependency"] = crop_dependency

    climate_alignment = analyze_climate_alignment(
        result["suitable_crops"],
        result["climate"],
        result["crops_used_in_recipes"]
    )
    result["climate_alignment"] = climate_alignment

    summary = generate_cultural_insights(
        country,
        result["climate"],
        crop_dependency,
        climate_alignment
    )
    result["analysis_summary"] = summary

    return result
