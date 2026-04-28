import pandas as pd
import numpy as np
from pathlib import Path

FEATURE_COLUMNS = [
    'temperature_2m', 'humidity', 'dewpoint_2m', 'apparent_temperature',
    'pressure', 'precipitation',
    'tithi_index', 'nakshatra_index', 'yoga_index', 'karana_index', 'vara_index',
    'moon_phase_angle', 'moon_distance_km', 'sun_lon', 'moon_lon',
    'day', 'month', 'dayofweek',
    'month_sin', 'month_cos',
    'is_monsoon', 'is_summer', 'is_winter',
    'rain_lag_1', 'rain_lag_3', 'rain_lag_6', 'rain_lag_12', 'rain_lag_24',
    'rain_sum_6', 'rain_sum_12', 'rain_sum_24',
    'rain_diff',
    'temp_humidity', 'temp_dewpoint', 'humidity_pressure', 'pressure_change',
    'temp_roll_6', 'humidity_roll_6', 'pressure_roll_6',
    'moon_phase_sin', 'moon_phase_cos', 'sun_moon_angle'
]

def load_past_data():
    path = Path("data/processed/weather_features.csv")
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def build_features(current_df, use_past_context=True):

    if use_past_context:
        past_df = load_past_data()
        df = pd.concat([past_df, current_df], ignore_index=True)
    else:
        df = current_df.copy()

    df["date"] = pd.to_datetime(df["date"])

    # TIME FEATURES
    df["day"] = df["date"].dt.day
    df["month"] = df["date"].dt.month
    df["dayofweek"] = df["date"].dt.dayofweek

    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

    # SEASONS
    df["is_monsoon"] = df["month"].isin([6, 7, 8, 9]).astype(int)
    df["is_summer"] = df["month"].isin([3, 4, 5]).astype(int)
    df["is_winter"] = df["month"].isin([12, 1, 2]).astype(int)

    # LAG FEATURES
    df["rain_lag_1"] = df["precipitation"].shift(1)
    df["rain_lag_3"] = df["precipitation"].shift(3)
    df["rain_lag_6"] = df["precipitation"].shift(6)
    df["rain_lag_12"] = df["precipitation"].shift(12)
    df["rain_lag_24"] = df["precipitation"].shift(24)

    # ROLLING
    df["rain_sum_6"] = df["precipitation"].rolling(6).sum()
    df["rain_sum_12"] = df["precipitation"].rolling(12).sum()
    df["rain_sum_24"] = df["precipitation"].rolling(24).sum()

    df["rain_diff"] = df["precipitation"].diff()

    # INTERACTIONS
    df["temp_humidity"] = df["temperature_2m"] * df["humidity"]
    df["temp_dewpoint"] = df["temperature_2m"] - df["dewpoint_2m"]
    df["humidity_pressure"] = df["humidity"] * df["pressure"]
    df["pressure_change"] = df["pressure"].diff()

    # ROLLING WEATHER
    df["temp_roll_6"] = df["temperature_2m"].rolling(6).mean()
    df["humidity_roll_6"] = df["humidity"].rolling(6).mean()
    df["pressure_roll_6"] = df["pressure"].rolling(6).mean()

    # ASTRONOMY
    df["moon_phase_sin"] = np.sin(np.radians(df["moon_phase_angle"]))
    df["moon_phase_cos"] = np.cos(np.radians(df["moon_phase_angle"]))
    df["sun_moon_angle"] = abs(df["sun_lon"] - df["moon_lon"])

    # CLEAN
    df = df.bfill().ffill()

    latest = df.iloc[[-1]]
    

    # return latest.select_dtypes(include=["number"])
    # Ensure all required features exist
    for col in FEATURE_COLUMNS:
        if col not in latest.columns:
            latest[col] = 0

    # Keep ONLY trained features in correct order
    latest = latest.reindex(columns=FEATURE_COLUMNS, fill_value=0)
    # 🔥 Remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]
    latest = latest.loc[:, ~latest.columns.duplicated()]
    return latest

# from pyexpat import model



# import pandas as pd
# import numpy as np
# from pathlib import Path

# FEATURE_COLUMNS = [
#     'temperature_2m', 'humidity', 'dewpoint_2m', 'apparent_temperature',
#     'pressure', 'precipitation',
#     'tithi_index', 'nakshatra_index', 'yoga_index', 'karana_index', 'vara_index',
#     'moon_phase_angle', 'moon_distance_km', 'sun_lon', 'moon_lon',
#     'day', 'month', 'dayofweek',
#     'month_sin', 'month_cos',
#     'is_monsoon', 'is_summer', 'is_winter',
#     'rain_lag_1', 'rain_lag_3', 'rain_lag_6', 'rain_lag_12', 'rain_lag_24',
#     'rain_sum_6', 'rain_sum_12', 'rain_sum_24',
#     'rain_diff',
#     'temp_humidity', 'temp_dewpoint', 'humidity_pressure', 'pressure_change',
#     'temp_roll_6', 'humidity_roll_6', 'pressure_roll_6',
#     'moon_phase_sin', 'moon_phase_cos', 'sun_moon_angle'
# ]


# def load_past_data():
#     path = Path("data/processed/weather_features.csv")
#     df = pd.read_csv(path)
#     df["date"] = pd.to_datetime(df["date"])
#     return df


# def build_features(current_df):
#     past_df = load_past_data()

#     # combine past + current
#     df = pd.concat([past_df, current_df], ignore_index=True)

#     df["date"] = pd.to_datetime(df["date"])

#     # ---------------- TIME ----------------
#     df["day"] = df["date"].dt.day
#     df["month"] = df["date"].dt.month
#     df["dayofweek"] = df["date"].dt.dayofweek

#     df["month_sin"] = np.sin(2*np.pi*df["month"]/12)
#     df["month_cos"] = np.cos(2*np.pi*df["month"]/12)

#     # ---------------- SEASON ----------------
#     df["is_monsoon"] = df["month"].isin([6,7,8,9]).astype(int)
#     df["is_summer"] = df["month"].isin([3,4,5]).astype(int)
#     df["is_winter"] = df["month"].isin([12,1,2]).astype(int)

#     # ---------------- LAG ----------------
#     df["rain_lag_1"] = df["precipitation"].shift(1)
#     df["rain_lag_3"] = df["precipitation"].shift(3)
#     df["rain_lag_6"] = df["precipitation"].shift(6)
#     df["rain_lag_12"] = df["precipitation"].shift(12)
#     df["rain_lag_24"] = df["precipitation"].shift(24)

#     # ---------------- ROLLING ----------------
#     df["rain_sum_6"] = df["precipitation"].rolling(6).sum()
#     df["rain_sum_12"] = df["precipitation"].rolling(12).sum()
#     df["rain_sum_24"] = df["precipitation"].rolling(24).sum()

#     df["rain_diff"] = df["precipitation"].diff()

#     # ---------------- INTERACTIONS ----------------
#     df["temp_humidity"] = df["temperature_2m"] * df["humidity"]
#     df["temp_dewpoint"] = df["temperature_2m"] - df["dewpoint_2m"]
#     df["humidity_pressure"] = df["humidity"] * df["pressure"]
#     df["pressure_change"] = df["pressure"].diff()

#     # ---------------- ROLLING WEATHER ----------------
#     df["temp_roll_6"] = df["temperature_2m"].rolling(6).mean()
#     df["humidity_roll_6"] = df["humidity"].rolling(6).mean()
#     df["pressure_roll_6"] = df["pressure"].rolling(6).mean()

#     # ---------------- ASTRONOMY ----------------
#     df["moon_phase_sin"] = np.sin(np.radians(df["moon_phase_angle"]))
#     df["moon_phase_cos"] = np.cos(np.radians(df["moon_phase_angle"]))
#     df["sun_moon_angle"] = abs(df["sun_lon"] - df["moon_lon"])

#     # ---------------- CLEAN ----------------
#     df = df.bfill().ffill()

#     # take latest row only
#     latest = df.iloc[[-1]]
    

#     # ensure exact feature match
#     latest = latest.reindex(columns=FEATURE_COLUMNS, fill_value=0)
#     for col in FEATURE_COLUMNS:
#         if col not in latest.columns:
#             latest[col] = 0
    
#     return latest