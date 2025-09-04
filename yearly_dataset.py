import pandas as pd

# Load datasets
tree_cover = pd.read_csv("filtered_datasets/filtered_tree_cover.csv")
co2_data = pd.read_csv("filtered_datasets/filtered_co2_data.csv")
weather = pd.read_csv("filtered_datasets/weather_data.csv")

# -------------------------
# 1. Process Weather Data
# -------------------------
# Convert Date column to datetime
weather["Date"] = pd.to_datetime(weather["Date"], format="%d-%m-%Y")

# Extract year
weather["Year"] = weather["Date"].dt.year

# Aggregate to yearly level
weather_yearly = weather.groupby(["Country", "Year"]).agg({
    "Temp_Max": "max",
    "Temp_Min": "min",
    "Temp_Mean": "mean",
    "Precipitation_Sum": "sum",
    "Windspeed_Max": "max",
    "Windgusts_Max": "max",
    "Sunshine_Duration": "sum"
}).reset_index()

# Keep only 2001–2023
weather_yearly = weather_yearly[(weather_yearly["Year"] >= 2001) & (weather_yearly["Year"] <= 2023)]

# -------------------------
# 2. Process Tree Cover Data
# -------------------------
tree_cover_filtered = tree_cover[
    (tree_cover["tree_cover_loss__year"] >= 2001) &
    (tree_cover["tree_cover_loss__year"] <= 2023)
]

# -------------------------
# 3. Process CO₂ Data
# -------------------------
co2_filtered = co2_data[
    (co2_data["year"] >= 2001) &
    (co2_data["year"] <= 2023)
]

# -------------------------
# Save results
# -------------------------
weather_yearly.to_csv("weather_yearly_2001_2023.csv", index=False)
tree_cover_filtered.to_csv("tree_cover_2001_2023.csv", index=False)
co2_filtered.to_csv("co2_2001_2023.csv", index=False)

print("✅ Consolidation complete. Files saved as:")
print(" - weather_yearly_2001_2023.csv")
print(" - tree_cover_2001_2023.csv")
print(" - co2_2001_2023.csv")
