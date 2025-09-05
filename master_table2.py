import pandas as pd
import numpy as np
 
# --------------------
# 0) Load processed datasets (unchanged)
# --------------------
weather    = pd.read_csv("yearly_dataset(final)/weather_yearly_2001_2023.csv")
tree_cover = pd.read_csv("yearly_dataset(final)/tree_cover_2001_2023.csv")
co2        = pd.read_csv("yearly_dataset(final)/co2_2001_2023.csv")
 
# --------------------
# 1) Standardize Units (weather as you had)
# --------------------
# Convert sunshine from seconds to hours (if your weather source is in seconds)
weather["Sunshine_Duration"] = weather["Sunshine_Duration"] / 3600.0
 
# --------------------
# 1b) CO2 unit harmonization (robust & safe)
#     Goal: ensure co2, coal_co2, oil_co2, gas_co2, cement_co2 are in **Mt**
#     We infer scale using population + an existing co2_per_capita (t/person),
#     so we can avoid brittle max<1000 heuristics.
# --------------------
def harmonize_co2_units_to_Mt(df):
    cols = [c for c in ["co2", "coal_co2", "oil_co2", "gas_co2", "cement_co2"] if c in df.columns]
    if {"co2", "population", "co2_per_capita"}.issubset(df.columns):
        # If co2 is in Mt, (co2 * 1e6 / population) should match t/person.
        implied_t_per_person = (df["co2"] * 1_000_000) / df["population"]
        ratio = np.nanmedian(implied_t_per_person / df["co2_per_capita"])
        # Heuristic interpretation:
        # ~1    => co2 already in Mt  (OK)
        # ~1000 => co2 was Gt -> needs *1000 to become Mt
        # ~1e-6 => co2 was tonnes -> needs /1e6 to become Mt
        if ratio > 100:                     # co2 likely in Gt
            for c in cols:
                df[c] = df[c] * 1_000.0
            print("[INFO] CO2 columns converted Gt → Mt (x1000) based on per-capita inference.")
        elif ratio < 0.01:                  # co2 likely in tonnes
            for c in cols:
                df[c] = df[c] / 1_000_000.0
            print("[INFO] CO2 columns converted tonnes → Mt (/1e6) based on per-capita inference.")
        else:
            print("[INFO] CO2 columns already in Mt (no unit change).")
    else:
        print("[WARN] Skipping CO2 unit inference (need 'co2','population','co2_per_capita').")
    return df
 
co2 = harmonize_co2_units_to_Mt(co2)
 
# --------------------
# 2) Handle Missing Values (your choices kept commented)
# --------------------
# weather = weather.fillna(method="ffill")
# co2     = co2.fillna(method="ffill")
# tree_cover = tree_cover.fillna(0)
 
# --------------------
# 3) Join Datasets (keep your renames exactly as requested)
# --------------------
co2.rename(columns={"year": "Year", "Country": "Country"}, inplace=True)  # leave as-is per your note
tree_cover.rename(columns={"tree_cover_loss__year": "Year"}, inplace=True)
 
master = (
    weather
    .merge(co2, on=["Country", "Year"], how="inner")
    .merge(tree_cover, on=["Country", "Year"], how="inner")
)
 
# --------------------
# 4) Derive New Metrics (CO2 + deforestation + anomaly)
# --------------------
 
# ---- CO2 per-capita (units: tonnes/person)
if {"co2", "population"}.issubset(master.columns):
    master["co2_per_capita_calc"] = (master["co2"] * 1_000_000) / master["population"]
else:
    raise ValueError("Missing 'co2' and/or 'population' to compute co2_per_capita_calc.")
 
# ---- CO2 growth metrics
master = master.sort_values(["Country", "Year"])
if {"Country", "Year", "co2"}.issubset(master.columns):
    master["co2_growth_abs"]  = master.groupby("Country")["co2"].diff()                  # Mt
    master["co2_growth_prct"] = master.groupby("Country")["co2"].pct_change() * 100.0   # %
    # Keep your column name but ensure it's correct & in sync
    master["co2_change_pct"]  = master["co2_growth_prct"]
 
# ---- (Optional) CO2 intensity per GDP if present (kg per 2011 international-$)
#      1 Mt = 1e9 kg
if {"co2", "gdp"}.issubset(master.columns):
    master["co2_per_gdp_kg_per_intl$"] = (master["co2"] * 1_000_000_000) / master["gdp"]
 
# ---- Deforestation %
if {"tree_cover_loss__ha", "tree_cover_extent_2000__ha"}.issubset(master.columns):
    master["deforestation_pct"] = (
        master["tree_cover_loss__ha"] / master["tree_cover_extent_2000__ha"] * 100.0
    )
 
# ---- Temperature anomaly vs 2001–2005 baseline (vectorized, safe for missing baselines)
if "Temp_Mean" in master.columns:
    baseline = (
        master.loc[master["Year"].between(2001, 2005)]
              .groupby("Country")["Temp_Mean"]
              .mean()
    )
    master["temp_anomaly"] = master["Temp_Mean"] - master["Country"].map(baseline)
 
# --------------------
# 5) Save transformed dataset
# --------------------
master.to_csv("master_climate_transformed2.csv", index=False)
print("Transformation complete. File saved as master_climate_transformed2.csv")
 
# --------------------
# 6) Quick QA prints (optional)
# --------------------
if "co2_per_capita" in master.columns:
    diff = (master["co2_per_capita"] - master["co2_per_capita_calc"]).abs()
    print(f"Per-capita CO2 abs diff | median={diff.median():.4f} t/person, max={diff.max():.4f} t/person")