import pandas as pd

# Load datasets
tree_cover = pd.read_csv("clean_datasets/consolidated_tree_cover_cleaned.csv")
co2_data = pd.read_csv("clean_datasets/filtered_co2_data.csv")
weather = pd.read_csv("clean_datasets/weather_data.csv")

# Get list of unique countries from weather data
weather_countries = weather["Country"].unique()

# Filter datasets by countries present in weather
tree_cover_filtered = tree_cover[tree_cover["Country Name"].isin(weather_countries)]
co2_filtered = co2_data[co2_data["country"].isin(weather_countries)]
weather_filtered = weather[weather["Country"].isin(weather_countries)]

# Save results (no renaming or other cleaning)
tree_cover_filtered.to_csv("filtered_tree_cover.csv", index=False)
co2_filtered.to_csv("filtered_co2_data.csv", index=False)
weather_filtered.to_csv("filtered_weather_data.csv", index=False)

print("✅ Datasets filtered by weather countries. Saved as:")
print(" - filtered_tree_cover.csv")
print(" - filtered_co2_data.csv")
print(" - filtered_weather_data.csv")