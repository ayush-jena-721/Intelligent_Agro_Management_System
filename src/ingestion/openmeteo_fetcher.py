import requests
import pandas as pd
from datetime import datetime, timedelta
import os

from src.config.settings import (
    TARGET_LAT,
    TARGET_LON,
    WEATHER_DATASET,
)
# This module fetches historical weather data from Open-Meteo API for the target location and compiles it into a single CSV dataset.
BASE_URL = "https://archive-api.open-meteo.com/v1/era5"
# If your account or use-case requires a different endpoint, change accordingly.
HOURLY_VARS = [
    "temperature_2m",
    "relativehumidity_2m",
    "dewpoint_2m",
    "apparent_temperature",
    "surface_pressure",
    "precipitation"
]

# Fetch hourly weather data for a given year
def fetch_year(lat, lon, start, end):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "hourly": ",".join(HOURLY_VARS),
        "timezone": "UTC"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise Exception("API request failed")
    data = response.json()
    df = pd.DataFrame(data["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    return df

# Convert hourly data to daily by aggregating
def convert_hourly_to_daily(df):
    df["date"] = df["time"].dt.date

# For temperature and humidity, we take the daily mean. For precipitation, we take the daily sum.
    daily = df.groupby("date").agg({
        "temperature_2m": "mean",
        "relativehumidity_2m": "mean",
        "dewpoint_2m": "mean",
        "apparent_temperature": "mean",
        "surface_pressure": "mean",
        "precipitation": "sum"
    }).reset_index()

# Rename columns for clarity
    daily = daily.rename(columns={
        "relativehumidity_2m": "humidity",
        "surface_pressure": "pressure"
    })
    return daily

# Main function to build the weather dataset
def build_weather_dataset():
    all_frames = []
    for year in range(1940, 2026):
        start = f"{year}-01-01"
        end = f"{year}-12-31"
        print("Fetching:", year)
        df = fetch_year(TARGET_LAT, TARGET_LON, start, end)
        daily = convert_hourly_to_daily(df)
        all_frames.append(daily)
    final_df = pd.concat(all_frames)
    os.makedirs(os.path.dirname(WEATHER_DATASET), exist_ok=True)
    final_df.to_csv(WEATHER_DATASET, index=False)
    print("Weather dataset saved:", WEATHER_DATASET)

# Example usage:
if __name__ == "__main__":
    build_weather_dataset()