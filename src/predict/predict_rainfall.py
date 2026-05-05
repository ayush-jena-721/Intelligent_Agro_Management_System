import pandas as pd
import joblib
import numpy as np

print("\n====== MEGHDRISTI MULTI-DAY FORECAST ======\n")

# -----------------------------
# Load model
# -----------------------------

model = joblib.load("models/lightgbm_rainfall_model.pkl")

# -----------------------------
# Load dataset
# -----------------------------

df = pd.read_csv("data/processed/weather_features.csv")

drop_cols = ["date","rainfall","hour","hour_sin","hour_cos"]

X = df.drop(columns=drop_cols)

latest_features = X.iloc[-1:].copy()

# -----------------------------
# Rainfall condition function
# -----------------------------

def rain_condition(value):

    if value == 0:
        return "No Rain ☀️"

    elif value < 2:
        return "Light Drizzle 🌦"

    elif value < 10:
        return "Light Rain 🌧"

    elif value < 50:
        return "Moderate Rain ⛈"

    else:
        return "Heavy Rain ⚡🌧"


# -----------------------------
# Multi-day forecast
# -----------------------------

forecast_days = 5

for day in range(1, forecast_days + 1):

    prediction = model.predict(latest_features)[0]

    prediction = max(0, prediction)

    condition = rain_condition(prediction)

    print(f"Day {day} Forecast")
    print("Rainfall:", round(prediction,2), "mm")
    print("Condition:", condition)
    print("--------------------------")

    # Update lag feature for next prediction
    if "rain_lag_1" in latest_features.columns:
        latest_features["rain_lag_1"] = prediction