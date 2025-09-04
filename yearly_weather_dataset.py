import requests
import csv
import time
import pandas as pd

import sys
sys.stdout.reconfigure(encoding='utf-8')


countries_coordinates = [
    # {"country": "India", "lat": 20.5937, "lon": 78.9629},
    # {"country": "China", "lat": 35.8617, "lon": 104.1954},
    {"country": "United States", "lat": 37.0902, "lon": -95.7129},
    {"country": "Indonesia", "lat": -0.7893, "lon": 113.9213},
    {"country": "Pakistan", "lat": 30.3753, "lon": 69.3451},
    {"country": "Brazil", "lat": -14.2350, "lon": -51.9253},
    {"country": "Nigeria", "lat": 9.0820, "lon": 8.6753},
    {"country": "Bangladesh", "lat": 23.6850, "lon": 90.3563},
    {"country": "Russia", "lat": 61.5240, "lon": 105.3188},
    {"country": "Mexico", "lat": 23.6345, "lon": -102.5528},
    {"country": "Japan", "lat": 36.2048, "lon": 138.2529},
    {"country": "Ethiopia", "lat": 9.1450, "lon": 40.4897},
    {"country": "Philippines", "lat": 13.4100, "lon": 122.5600},
    {"country": "Egypt", "lat": 26.8206, "lon": 30.8025},
    {"country": "Vietnam", "lat": 14.0583, "lon": 108.2772},
    {"country": "DR Congo", "lat": -4.0383, "lon": 21.7587},
    {"country": "Turkey", "lat": 38.9637, "lon": 35.2433},
    {"country": "Iran", "lat": 32.4279, "lon": 53.6880},
    {"country": "Germany", "lat": 51.1657, "lon": 10.4515},
    {"country": "Thailand", "lat": 15.8700, "lon": 100.9925},
    {"country": "United Kingdom", "lat": 55.3781, "lon": -3.4360},
    {"country": "France", "lat": 46.2276, "lon": 2.2137},
    {"country": "Italy", "lat": 41.8719, "lon": 12.5674},
    {"country": "South Africa", "lat": -30.5595, "lon": 22.9375},
    {"country": "Tanzania", "lat": -6.3690, "lon": 34.8888},
    {"country": "Myanmar", "lat": 21.9162, "lon": 95.9560},
    {"country": "South Korea", "lat": 35.9078, "lon": 127.7669},
    {"country": "Colombia", "lat": 4.5709, "lon": -74.2973},
    {"country": "Kenya", "lat": -0.0236, "lon": 37.9062},
    {"country": "Spain", "lat": 40.4637, "lon": -3.7492},
    {"country": "Argentina", "lat": -38.4161, "lon": -63.6167},
    {"country": "Algeria", "lat": 28.0339, "lon": 1.6596},
    {"country": "Sudan", "lat": 12.8628, "lon": 30.2176},
    {"country": "Ukraine", "lat": 48.3794, "lon": 31.1656},
    {"country": "Uganda", "lat": 1.3733, "lon": 32.2903},
    {"country": "Iraq", "lat": 33.2232, "lon": 43.6793},
    {"country": "Poland", "lat": 51.9194, "lon": 19.1451},
    {"country": "Canada", "lat": 56.1304, "lon": -106.3468},
    {"country": "Morocco", "lat": 31.7917, "lon": -7.0926},
    {"country": "Saudi Arabia", "lat": 23.8859, "lon": 45.0792},
    {"country": "Uzbekistan", "lat": 41.3775, "lon": 64.5853},
    {"country": "Malaysia", "lat": 4.2105, "lon": 101.9758},
    {"country": "Peru", "lat": -9.1900, "lon": -75.0152},
    {"country": "Afghanistan", "lat": 33.9391, "lon": 67.7100},
    {"country": "Venezuela", "lat": 6.4238, "lon": -66.5897},
    {"country": "Nepal", "lat": 28.3949, "lon": 84.1240},
    {"country": "Ghana", "lat": 7.9465, "lon": -1.0232},
    {"country": "Yemen", "lat": 15.5527, "lon": 48.5164},
    {"country": "Mozambique", "lat": -18.6657, "lon": 35.5296},
    {"country": "North Korea", "lat": 40.3399, "lon": 127.5101},
    {"country": "Madagascar", "lat": -18.7669, "lon": 46.8691},
    {"country": "Australia", "lat": -25.2744, "lon": 133.7751},
    {"country": "Cameroon", "lat": 7.3697, "lon": 12.3547},
    {"country": "Niger", "lat": 17.6078, "lon": 8.0817},
    {"country": "Sri Lanka", "lat": 7.8731, "lon": 80.7718},
    {"country": "Burkina Faso", "lat": 12.2383, "lon": -1.5616},
    {"country": "Mali", "lat": 17.5707, "lon": -3.9962},
    {"country": "Romania", "lat": 45.9432, "lon": 24.9668},
    {"country": "Malawi", "lat": -13.2543, "lon": 34.3015},
    {"country": "Chile", "lat": -35.6751, "lon": -71.5430},
    {"country": "Kazakhstan", "lat": 48.0196, "lon": 66.9237},
    {"country": "Zambia", "lat": -13.1339, "lon": 27.8493},
    {"country": "Guatemala", "lat": 15.7835, "lon": -90.2308},
    {"country": "Ecuador", "lat": -1.8312, "lon": -78.1834},
    {"country": "Netherlands", "lat": 52.1326, "lon": 5.2913},
    {"country": "Syria", "lat": 34.8021, "lon": 38.9968},
    {"country": "Cambodia", "lat": 12.5657, "lon": 104.9910},
    {"country": "Senegal", "lat": 14.4974, "lon": -14.4524},
    {"country": "Chad", "lat": 15.4542, "lon": 18.7322},
    {"country": "Somalia", "lat": 5.1521, "lon": 46.1996},
    {"country": "Zimbabwe", "lat": -19.0154, "lon": 29.1549},
    {"country": "Guinea", "lat": 9.9456, "lon": -9.6966},
    {"country": "Rwanda", "lat": -1.9403, "lon": 29.8739},
    {"country": "Benin", "lat": 9.3077, "lon": 2.3158},
    {"country": "Burundi", "lat": -3.3731, "lon": 29.9189},
    {"country": "Tunisia", "lat": 33.8869, "lon": 9.5375},
    {"country": "Bolivia", "lat": -16.2902, "lon": -63.5887},
    {"country": "Belgium", "lat": 50.5039, "lon": 4.4699},
    {"country": "Haiti", "lat": 18.9712, "lon": -72.2852},
    {"country": "Cuba", "lat": 21.5218, "lon": -77.7812},
    {"country": "South Sudan", "lat": 6.8769, "lon": 31.3069},
    {"country": "Dominican Republic", "lat": 18.7357, "lon": -70.1627},
    {"country": "Czech Republic", "lat": 49.8175, "lon": 15.4730},
    {"country": "Greece", "lat": 39.0742, "lon": 21.8243},
    {"country": "Jordan", "lat": 30.5852, "lon": 36.2384},
    {"country": "Portugal", "lat": 39.3999, "lon": -8.2245},
    {"country": "Azerbaijan", "lat": 40.1431, "lon": 47.5769},
    {"country": "Sweden", "lat": 60.1282, "lon": 18.6435},
    {"country": "Honduras", "lat": 15.2000, "lon": -86.2419},
    {"country": "United Arab Emirates", "lat": 23.4241, "lon": 53.8478},
    {"country": "Hungary", "lat": 47.1625, "lon": 19.5033},
    {"country": "Tajikistan", "lat": 38.8610, "lon": 71.2761},
    {"country": "Belarus", "lat": 53.7098, "lon": 27.9534},
    {"country": "Austria", "lat": 47.5162, "lon": 14.5501},
    {"country": "Papua New Guinea", "lat": -6.314993, "lon": 143.9555},
    {"country": "Serbia", "lat": 44.0165, "lon": 21.0059},
    {"country": "Israel", "lat": 31.0461, "lon": 34.8516},
    {"country": "Switzerland", "lat": 46.8182, "lon": 8.2275},
    {"country": "Togo", "lat": 8.6195, "lon": 0.8248},
    {"country": "Sierra Leone", "lat": 8.4606, "lon": -11.7799},
    {"country": "Laos", "lat": 19.8563, "lon": 102.4955},
    {"country": "Paraguay", "lat": -23.4425, "lon": -58.4438},
    {"country": "Bulgaria", "lat": 42.7339, "lon": 25.4858},
    {"country": "Libya", "lat": 26.3351, "lon": 17.2283},
    {"country": "Lebanon", "lat": 33.8547, "lon": 35.8623}
]

# Open-Meteo API endpoint
base_url = "https://archive-api.open-meteo.com/v1/archive"
output_filename = "weather_datasets/consolidated_yearly_weather_data.csv"

with open(output_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Country", "Year", "Temp_Max", "Temp_Min", "Temp_Mean",
        "Precipitation_Sum", "Windspeed_Max", "Windgusts_Max", "Sunshine_Duration"
    ])

    for entry in countries_coordinates:
        country = entry["country"]
        lat = entry["lat"]
        lon = entry["lon"]

        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": "2000-01-01",
            "end_date": "2023-12-31",
            "daily": [
                "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
                "precipitation_sum", "windspeed_10m_max", "windgusts_10m_max", "sunshine_duration"
            ],
            "timezone": "auto",
            "models": "era5" # ensures global coverage
        }

        print(f"Fetching daily data for {country}...")
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            daily = data.get("daily", {})
            if not daily:
                print(f"No data for {country}")
                continue

            df = pd.DataFrame(daily)
            df["time"] = pd.to_datetime(df["time"])
            df["year"] = df["time"].dt.year

            # Aggregate daily → yearly
            yearly = df.groupby("year").agg({
                "temperature_2m_max": "mean",
                "temperature_2m_min": "mean",
                "temperature_2m_mean": "mean",
                "precipitation_sum": "sum",
                "windspeed_10m_max": "max",
                "windgusts_10m_max": "max",
                "sunshine_duration": "sum"
            }).reset_index()

            for _, row in yearly.iterrows():
                writer.writerow([
                    country, row["year"], row["temperature_2m_max"], row["temperature_2m_min"],
                    row["temperature_2m_mean"], row["precipitation_sum"], row["windspeed_10m_max"],
                    row["windgusts_10m_max"], row["sunshine_duration"]
                ])

            print(f"Added yearly aggregated data for {country}")
        else:
            print(f"Failed for {country}. Status: {response.status_code}")

        time.sleep(1) # polite delay

print(f"Saved yearly consolidated weather data to {output_filename}")