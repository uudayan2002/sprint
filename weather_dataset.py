import requests
import csv
import time
 
# List of top 100 countries with central coordinates
countries_coordinates = [
    # {"country": "India", "lat": 20.5937, "lon": 78.9629},
    # {"country": "China", "lat": 35.8617, "lon": 104.1954},
    # {"country": "United States", "lat": 37.0902, "lon": -95.7129},
    # {"country": "Indonesia", "lat": -0.7893, "lon": 113.9213},
    # {"country": "Pakistan", "lat": 30.3753, "lon": 69.3451},
    # {"country": "Nigeria", "lat": 9.0820, "lon": 8.6753},
    # {"country": "Bangladesh", "lat": 23.6850, "lon": 90.3563},
    # {"country": "Russia", "lat": 61.5240, "lon": 105.3188},
    # {"country": "Mexico", "lat": 23.6345, "lon": -102.5528},
    # {"country": "Japan", "lat": 36.2048, "lon": 138.2529},
    # {"country": "Ethiopia", "lat": 9.1450, "lon": 40.4897},
    # {"country": "Philippines", "lat": 13.4100, "lon": 122.5600},
    # {"country": "Egypt", "lat": 26.8206, "lon": 30.8025},
    # {"country": "Vietnam", "lat": 14.0583, "lon": 108.2772},
    # {"country": "Iran", "lat": 32.4279, "lon": 53.6880},
    # {"country": "Germany", "lat": 51.1657, "lon": 10.4515},
    # {"country": "Thailand", "lat": 15.8700, "lon": 100.9925},
    # {"country": "United Kingdom", "lat": 55.3781, "lon": -3.4360},
    # {"country": "France", "lat": 46.2276, "lon": 2.2137},
    # {"country": "Italy", "lat": 41.8719, "lon": 12.5674},
    # {"country": "South Africa", "lat": -30.5595, "lon": 22.9375},
    # {"country": "Tanzania", "lat": -6.3690, "lon": 34.8888},
    # {"country": "Myanmar", "lat": 21.9162, "lon": 95.9560},
    # {"country": "DR Congo", "lat": -4.0383, "lon": 21.7587},
    # {"country": "Turkey", "lat": 38.9637, "lon": 35.2433},
]
 
# Open-Meteo API endpoint
base_url = "https://archive-api.open-meteo.com/v1/archive"
 
# Loop through each country
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
        "timezone": "auto"
    }
 
    print(f"Fetching data for {country}...")
    response = requests.get(base_url, params=params)
 
    if response.status_code == 200:
        data = response.json()
        dates = data["daily"]["time"]
        rows = zip(
            dates,
            data["daily"].get("temperature_2m_max", []),
            data["daily"].get("temperature_2m_min", []),
            data["daily"].get("temperature_2m_mean", []),
            data["daily"].get("precipitation_sum", []),
            data["daily"].get("windspeed_10m_max", []),
            data["daily"].get("windgusts_10m_max", []),
            data["daily"].get("sunshine_duration", [])
        )
 
        filename = f"weather_datasets/{country.replace(' ', '_')}_weather_data.csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Date", "Temp_Max", "Temp_Min", "Temp_Mean",
                "Precipitation_Sum", "Windspeed_Max", "Windgusts_Max", "Sunshine_Duration"
            ])
            writer.writerows(rows)
 
        print(f"Saved weather data for {country} to {filename}")
    else:
        print(f"Failed to fetch data for {country}. Status code: {response.status_code}")
 
    time.sleep(1)  # Avoid rate limiting
 