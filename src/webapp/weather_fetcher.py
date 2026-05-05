import requests
import pandas as pd

def fetch_current_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "dewpoint_2m",
            "pressure_msl",
            "precipitation"
        ],
        "forecast_days": 1,
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame({
        "date": data["hourly"]["time"],
        "temperature_2m": data["hourly"]["temperature_2m"],
        "humidity": data["hourly"]["relative_humidity_2m"],
        "dewpoint_2m": data["hourly"]["dewpoint_2m"],
        "pressure": data["hourly"]["pressure_msl"],
        "precipitation": data["hourly"]["precipitation"]
    })

    df["date"] = pd.to_datetime(df["date"]).dt.floor("h")

    return df.iloc[[-1]]  # latest only