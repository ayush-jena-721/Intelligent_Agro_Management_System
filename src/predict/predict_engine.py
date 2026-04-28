import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta

# ---------------------------------------
# LOAD MODEL
# ---------------------------------------

MODEL_PATH = "models/lightgbm_rainfall_model.pkl"
model = joblib.load(MODEL_PATH)

print("\n====== MEGHDRISTI PREDICTION ENGINE (v2) ======\n")


# ---------------------------------------
# UTILITY: CONDITION LOGIC
# ---------------------------------------

def rain_condition(rain: float) -> str:

    if rain <= 0.1:
        return "No Rain ☀️"
    elif rain < 2:
        return "Light Drizzle 🌦"
    elif rain < 10:
        return "Light Rain 🌧"
    elif rain < 50:
        return "Moderate Rain ⛈"
    else:
        return "Heavy Rain 🌧⚡"


def rain_probability(rain: float) -> int:

    if rain <= 0.1:
        return 10
    elif rain < 2:
        return 30
    elif rain < 10:
        return 60
    elif rain < 50:
        return 80
    else:
        return 95


# ---------------------------------------
# CORE: FEATURE ALIGNMENT
# ---------------------------------------

def align_features(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensures incoming data matches training features exactly
    """

    required_features = model.feature_name_

    for col in required_features:
        if col not in input_df.columns:
            input_df[col] = 0

    return input_df[required_features]


# ---------------------------------------
# CORE: SINGLE PREDICTION
# ---------------------------------------

def predict_rain(features_df: pd.DataFrame) -> float:

    X = align_features(features_df.copy())

    pred = model.predict(X)[0]

    return round(max(0, float(pred)), 2)


# ---------------------------------------
# FORECAST ENGINE (MULTI-DAY)
# ---------------------------------------

def forecast(features_df: pd.DataFrame, days: int = 5):

    results = []

    latest_features = features_df.copy()

    base_date = datetime.now()

    for day in range(1, days + 1):

        pred = predict_rain(latest_features)

        future_date = base_date + timedelta(days=day)

        result = {
            "date": future_date.strftime("%Y-%m-%d"),
            "day": day,
            "rainfall_mm": pred,
            "rain_probability": rain_probability(pred),
            "condition": rain_condition(pred)
        }

        results.append(result)

        # -----------------------------
        # Update lag features (IMPORTANT)
        # -----------------------------
        if "rain_lag_1" in latest_features.columns:
            latest_features.loc[:, "rain_lag_1"] = pred

    return results


# ---------------------------------------
# CURRENT WEATHER FORMATTER
# ---------------------------------------

def format_current_weather(latest_row: pd.Series) -> dict:

    return {
        "temperature": round(float(latest_row.get("temperature_2m", 0)), 2),
        "humidity": round(float(latest_row.get("humidity", 0)), 2),
        "pressure": round(float(latest_row.get("pressure", 0)), 2),
        "dewpoint": round(float(latest_row.get("dewpoint_2m", 0)), 2),
        "precipitation": round(float(latest_row.get("precipitation", 0)), 2),
        "tithi_index": int(latest_row.get("tithi_index", 0)),
        "nakshatra_index": int(latest_row.get("nakshatra_index", 0)),
        "yoga_index": int(latest_row.get("yoga_index", 0)),
        "karana_index": int(latest_row.get("karana_index", 0)),
        "moon_phase_angle": round(float(latest_row.get("moon_phase_angle", 0)), 2)
    }


# ---------------------------------------
# AGRICULTURE INSIGHT ENGINE
# ---------------------------------------

def agriculture_advice(rain: float, humidity: float) -> str:

    if rain > 5:
        return "Rain expected. Avoid irrigation."

    elif humidity > 75:
        return "High humidity. Monitor crops for fungal disease."

    else:
        return "Low rainfall predicted. Irrigation recommended."


# ---------------------------------------
# API WRAPPER FUNCTION (IMPORTANT)
# ---------------------------------------

def generate_forecast(features_df: pd.DataFrame) -> dict:
    """
    Main entry point for API
    """

    latest_row = features_df.iloc[0]

    weather = format_current_weather(latest_row)

    forecast_data = forecast(features_df, days=5)

    advice = agriculture_advice(
        forecast_data[0]["rainfall_mm"],
        weather["humidity"]
    )

    return {
        "current_weather": weather,
        "forecast": forecast_data,
        "agriculture_insight": advice
    }

# ---------------------------------------
# TEST MODE (CLI)
# ---------------------------------------

if __name__ == "__main__":

    # TEMP: using old dataset ONLY for testing
    df = pd.read_csv("data/processed/weather_features.csv")

    latest_row = df.iloc[-1]
    features_df = pd.DataFrame([latest_row])

    print("\n📊 Current Weather\n")

    weather = format_current_weather(latest_row)

    for k, v in weather.items():
        print(f"{k}: {v}")

    print("\n🌧 Forecast\n")

    forecast_data = forecast(features_df, days=5)

    for day in forecast_data:
        print(
            f"{day['date']} → "
            f"{day['rainfall_mm']} mm | "
            f"{day['rain_probability']}% | "
            f"{day['condition']}"
        )

    print("\n🌱 Agriculture Insight\n")

    advice = agriculture_advice(
        forecast_data[0]["rainfall_mm"],
        weather["humidity"]
    )

    print(advice)

