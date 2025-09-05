import pandas as pd

# Load processed datasets
weather = pd.read_csv("yearly_dataset(final)/weather_yearly_2001_2023.csv")
tree_cover = pd.read_csv("yearly_dataset(final)/tree_cover_2001_2023.csv")
co2 = pd.read_csv("yearly_dataset(final)/co2_2001_2023.csv")

# --------------------
# 1. Standardize Units
# --------------------
# Convert sunshine from seconds to hours
weather["Sunshine_Duration"] = weather["Sunshine_Duration"] / 3600  

# Convert CO2 emissions to MtCO₂ if in Gt (assuming dataset is in Gt)
if co2["co2"].max() < 1000: # heuristic check
    co2["co2"] = co2["co2"] * 1e3 # Gt → Mt
    co2["coal_co2"] = co2["coal_co2"] * 1e3
    co2["oil_co2"] = co2["oil_co2"] * 1e3
    co2["gas_co2"] = co2["gas_co2"] * 1e3
    co2["cement_co2"] = co2["cement_co2"] * 1e3

# --------------------
# 2. Handle Missing Values
# --------------------
# weather = weather.fillna(method="ffill") # forward fill
# co2 = co2.fillna(method="ffill")
# tree_cover = tree_cover.fillna(0)

# --------------------
# 3. Join Datasets
# --------------------
# Rename columns for consistency
co2.rename(columns={"year": "Year", "Country": "Country"}, inplace=True)
tree_cover.rename(columns={"tree_cover_loss__year": "Year"}, inplace=True)

# Merge on Country + Year
master = (
    weather
    .merge(co2, on=["Country", "Year"], how="inner")
    .merge(tree_cover, on=["Country", "Year"], how="inner")
)

# --------------------
# 4. Derive New Metrics
# --------------------
master["co2_per_capita_calc"] = master["co2"] / master["population"]
master["co2_change_pct"] = master.groupby("Country")["co2"].pct_change() * 100
master["deforestation_pct"] = (
    master["tree_cover_loss__ha"] / master["tree_cover_extent_2000__ha"] * 100
)

# Baseline temperature anomaly (vs 2001–2005 avg)
baseline = master[master["Year"].between(2001, 2005)].groupby("Country")["Temp_Mean"].mean()
master["temp_anomaly"] = master.apply(
    lambda row: row["Temp_Mean"] - baseline[row["Country"]], axis=1
)

# --------------------
# Save transformed dataset
# --------------------
master.to_csv("master_climate_transformed.csv", index=False)

print("Transformation complete. File saved as master_climate_transformed.csv")