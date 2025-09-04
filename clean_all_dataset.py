import pandas as pd

# Load datasets
tree_cover = pd.read_csv("filtered_datasets/filtered_tree_cover.csv")
co2_data = pd.read_csv("filtered_datasets/filtered_co2_data.csv")
weather = pd.read_csv("filtered_datasets/weather_data.csv")

# Get list of unique countries in weather data
weather_countries = weather["Country"].unique()

# Filter tree cover data (Country Name column)
tree_cover_filtered = tree_cover[tree_cover["Country Name"].isin(weather_countries)]

# Filter CO2 data (country column)
co2_filtered = co2_data[co2_data["country"].isin(weather_countries)]

# Save cleaned files
tree_cover_filtered.to_csv("filtered2_tree_cover.csv", index=False)
co2_filtered.to_csv("filtered2_co2_data.csv", index=False)

print("✅ Filtering complete. Files saved as 'filtered2_tree_cover.csv' and 'filtered2_co2_data.csv'.")
