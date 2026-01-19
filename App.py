import streamlit as st
from collections import Counter
from Analysis import analyze_all_cuisine, full_analyze_recipe
from Analysis import recipes_df
from difflib import get_close_matches
import matplotlib.pyplot as plt 


# ---------------- FUZZY RECIPE MATCH ----------------
def find_best_recipe_match(query, recipes_df):
    query = query.lower().strip()
    recipes = recipes_df["Recipe Name"].astype(str).str.lower().tolist()

    if query in recipes:
        return query

    partial = [r for r in recipes if query in r]
    if partial:
        return partial[0]

    close = get_close_matches(query, recipes, n=1, cutoff=0.55)
    if close:
        return close[0]

    return None


# ---------------- COUNTRY ALIASES ----------------
COUNTRY_ALIASES = {
    "united states of america": "united states",
    "usa": "united states",
    "us": "united states",
    "u.s.a.": "united states",
    "u.s.": "united states",
    "uk": "united kingdom",
    "uae": "united arab emirates",
}



# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FDCA - Food Diversity and Cultural Analysis",
    page_icon="🌍",
    layout="wide"
)



# ---------------- CSS ----------------
st.markdown("""
<style>

.tag {
    display:inline-flex;
    flex-wrap:wrap;
    padding:6px 10px;
    margin:4px;
    background:#222;
    color:#eee;
    border-radius:8px;
    font-size:14px;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    margin: 20px 0 8px 0;
    color: #f5f5f5;
}

.subtle {
    color:#aaa;
    font-size:14px;
}

.card {
    padding: 20px;
    margin-top: 12px;
    background-color: #111111;
    border-radius: 12px;
    border: 1px solid #333;
}

.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)



# ---------------- TAG HELPERS ----------------
def tagify(items):
    if not items:
        st.write("No data available.")
        return
    html = "".join([f"<span class='tag'>{i.title()}</span>" for i in items])
    st.markdown(html, unsafe_allow_html=True)



# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align:center;'>FDCA – Food Diversity & Cultural Analysis</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; font-size:18px;'>Search any <b>Country</b> or <b>Food Item</b> to begin.</p>",
    unsafe_allow_html=True
)

search_query = st.text_input("", placeholder="Search for Country or Food Item...")
search_button = st.button("Search")

st.divider()



# ---------------- EMPTY LANDING ----------------
if not search_query.strip():
    st.header("Welcome to FDCA")
    st.write("""
    - Search by **country** to explore climate, crops, and cuisine  
    - Search by **food** to trace ingredients and agricultural origins  
    - Designed to give **clean insights**, not messy raw data  
    """)
    st.stop()



# ---------------- SEARCH ACTION ----------------
if search_button:
    query = search_query.strip().lower()
    query = COUNTRY_ALIASES.get(query, query)

    with st.spinner("Analyzing..."):

        country_result = analyze_all_cuisine(query)



        # ---------------- FOOD SEARCH ----------------
        if country_result["climate"] is None:

            matched_recipe = find_best_recipe_match(query, recipes_df)

            if matched_recipe is None:
                st.error("No matching country or food item found. Please try a different query.")
                st.stop()

            recipe_result = full_analyze_recipe(matched_recipe)

            st.markdown(f"<div class='section-title'>🍽 {matched_recipe.title()}</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-title'>Ingredients</div>", unsafe_allow_html=True)
            tagify(recipe_result["ingredients"])

            st.markdown("<div class='section-title'>Crops Used</div>", unsafe_allow_html=True)
            tagify(recipe_result["crops"])



        # ---------------- COUNTRY SEARCH ----------------
        else:

            st.markdown(f"<div class='section-title'>🌍 {search_query.title()}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='subtle'>Climate: {country_result['climate']}</div>", unsafe_allow_html=True)

            # -------- Climate-Aligned Crops --------
            suitable = country_result["suitable_crops"]
            st.markdown("<div class='section-title'>🌱 Climate-Aligned Crops</div>", unsafe_allow_html=True)
            tagify(suitable[:8])

            if len(suitable) > 8:
                with st.expander("View all suitable crops"):
                    tagify(suitable)


            # -------- Recipes --------
            recipes = country_result["recipes"]
            st.markdown("<div class='section-title'>🍲 Common Recipes</div>", unsafe_allow_html=True)
            tagify(recipes[:5])

            if len(recipes) > 5:
                with st.expander("View all recipes"):
                    tagify(recipes)


            # -------- Crops Used --------
            dominant = country_result["crop_dependency"]["dominant_crops"]
            all_crops = country_result["crops_used_in_recipes"]

            st.markdown("<div class='section-title'>🌾 Key Crops Used</div>", unsafe_allow_html=True)
            tagify(dominant)

            if len(all_crops) > len(dominant):
                with st.expander("View full crop list"):
                    tagify(all_crops)


            # -------- Metrics --------
            local = country_result["crop_dependency"]["local_crops_used"]
            imported = country_result["crop_dependency"]["imported_crops_used"]
            fit = int(country_result["climate_alignment"]["alignment_score"] * 100)

            st.markdown("<div class='section-title'>📊 Local vs Imported</div>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("Local", local)
            c2.metric("Imported", imported)
            c3.metric("Climate Fit", f"{fit}%")

            st.markdown(
                "<p class='subtle'>This balance reflects how domestic farming and trade shape the cuisine.</p>",
                unsafe_allow_html=True
            )


            # -------- Cultural Insights --------
            st.markdown("<div class='section-title'>✨ Cultural Insights</div>", unsafe_allow_html=True)

            st.markdown(f"""
                <div class='card'>
                    <p style='font-size:16px; line-height:1.7;'>
                        {country_result['analysis_summary']}
                    </p>
                </div>
            """, unsafe_allow_html=True)



            # -------- AESTHETIC SIDE-BY-SIDE VISUALS --------
            with st.expander("📈 Visual Summary"):

                col1, col2 = st.columns(2)

                # ---------- PIE CHART ----------
                with col1:
                    fig1, ax1 = plt.subplots(figsize=(3.5, 2.5))

                    ax1.pie(
                        [local, imported],
                        labels=["Local", "Imported"],
                        autopct="%1.0f%%",
                        startangle=90,
                        pctdistance=0.75
                    )

                    ax1.axis("equal")
                    ax1.set_title("Local vs Imported", fontsize=11, pad=6)

                    st.pyplot(fig1)


                # ---------- CLIMATE ALIGNMENT ----------
                with col2:
                    fig2, ax2 = plt.subplots(figsize=(3.5, 2.5))

                    ax2.bar(["Aligned", "Misaligned"], [fit/100, 1-(fit/100)])

                    ax2.set_ylim(0, 1)
                    ax2.set_title("Climate Alignment", fontsize=11, pad=6)

                    for spine in ax2.spines.values():
                        spine.set_visible(False)

                    ax2.tick_params(labelsize=9)
                    plt.tight_layout()

                    st.pyplot(fig2)


                st.markdown("<div style='margin-top:15px'></div>", unsafe_allow_html=True)


                # ---------- TOP CROPS ----------
                crop_counts = Counter(country_result["crops_used_in_recipes"])
                top_crops = crop_counts.most_common(5)

                if top_crops:
                    crops, counts = zip(*top_crops)

                    fig3, ax3 = plt.subplots(figsize=(3.5, 2.5))

                    ax3.barh(crops, counts)
                    ax3.invert_yaxis()

                    ax3.set_title("Top Crops Used", fontsize=11, pad=6)

                    for spine in ax3.spines.values():
                        spine.set_visible(False)

                    ax3.tick_params(labelsize=9)
                    plt.tight_layout()

                    st.pyplot(fig3)
