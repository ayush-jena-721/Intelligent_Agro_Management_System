# import pandas as pd
# import numpy as np

# print("Loading dataset...")

# df = pd.read_csv("data/processed/clean_dataset.csv")
# df["date"] = pd.to_datetime(df["date"])

# df = df.sort_values("date").reset_index(drop=True)

# # --------------------------------------------------
# # 1. TIME FEATURES
# # --------------------------------------------------
# print("Creating time features...")

# df["year"] = df["date"].dt.year
# df["month"] = df["date"].dt.month
# df["day"] = df["date"].dt.day

# df["day_of_year"] = df["date"].dt.dayofyear

# # Leap year safe normalization
# df["days_in_year"] = df["date"].dt.is_leap_year.map({True:366, False:365})

# df["day_sin"] = np.sin(2 * np.pi * df["day_of_year"] / df["days_in_year"])
# df["day_cos"] = np.cos(2 * np.pi * df["day_of_year"] / df["days_in_year"])

# # Monsoon season indicator
# df["monsoon_flag"] = df["month"].isin([6,7,8,9]).astype(int)

# # --------------------------------------------------
# # 2. RAINFALL LAG FEATURES
# # --------------------------------------------------
# print("Creating rainfall lag features...")

# lag_days = [1,3,7,14]

# for lag in lag_days:
#     df[f"rain_lag{lag}"] = df["rainfall"].shift(lag)

# # --------------------------------------------------
# # 3. ROLLING RAINFALL FEATURES
# # --------------------------------------------------
# print("Creating rainfall rolling statistics...")

# roll_windows = [3,7,14,30]

# for window in roll_windows:

#     df[f"rain_roll{window}"] = (
#         df["rainfall"]
#         .rolling(window=window, min_periods=1)
#         .mean()
#     )

#     df[f"rain_std{window}"] = (
#         df["rainfall"]
#         .rolling(window=window, min_periods=1)
#         .std()
#     )

# # --------------------------------------------------
# # 4. TEMPERATURE & HUMIDITY ROLLING FEATURES
# # --------------------------------------------------
# print("Creating weather rolling features...")

# for window in [3,7]:

#     df[f"temp_roll{window}"] = (
#         df["temperature_2m"]
#         .rolling(window, min_periods=1)
#         .mean()
#     )

#     df[f"hum_roll{window}"] = (
#         df["humidity"]
#         .rolling(window, min_periods=1)
#         .mean()
#     )

# # --------------------------------------------------
# # 5. RAIN INTENSITY FEATURE
# # --------------------------------------------------
# # print("Creating rainfall intensity signal...")

# # df["heavy_rain"] = (df["rainfall"] > 20).astype(int)

# # --------------------------------------------------
# # 6. ASTRONOMY CIRCULAR ENCODING
# # --------------------------------------------------
# print("Encoding astronomical cycles...")

# df["sun_sin"] = np.sin(np.radians(df["sun_lon"]))
# df["sun_cos"] = np.cos(np.radians(df["sun_lon"]))

# df["moon_sin"] = np.sin(np.radians(df["moon_lon"]))
# df["moon_cos"] = np.cos(np.radians(df["moon_lon"]))

# df["phase_sin"] = np.sin(np.radians(df["moon_phase_angle"]))
# df["phase_cos"] = np.cos(np.radians(df["moon_phase_angle"]))

# # --------------------------------------------------
# # 7. ASTRONOMY INTERACTION FEATURES
# # --------------------------------------------------
# print("Creating astronomy interaction features...")

# df["moon_humidity"] = df["moon_phase_angle"] * df["humidity"]

# df["sun_temperature"] = df["sun_lon"] * df["temperature_2m"]

# if "nakshatra_index" in df.columns:
#     df["nakshatra_rain"] = df["nakshatra_index"] * df["rain_lag1"]

# # --------------------------------------------------
# # 8. CLEANUP
# # --------------------------------------------------
# print("Cleaning dataset...")

# df = df.drop(columns=[
#     "sun_lon",
#     "moon_lon",
#     "moon_phase_angle",
#     "days_in_year"
# ], errors="ignore")

# # Fill remaining NaNs
# df = df.bfill()
# df = df.fillna(0)

# # --------------------------------------------------
# # 9. SAVE FEATURE DATASET
# # --------------------------------------------------
# print("Saving feature dataset...")

# df.to_csv("data/processed/feature_dataset.csv", index=False)

# print("\nFeature engineering complete")
# print("Rows:", len(df))
# print("Columns:", len(df.columns))
# print("Dataset ready for ML training.")

import pandas as pd
import numpy as np
from pathlib import Path

print("Loading dataset...")

DATA_PATH = Path("data/processed/clean_dataset.csv")
SAVE_PATH = Path("data/processed/weather_features.csv")

df = pd.read_csv(DATA_PATH)

# -------------------------
# TIME FEATURES
# -------------------------

print("Creating time features...")

df["date"] = pd.to_datetime(df["date"])

df["hour"] = df["date"].dt.hour
df["day"] = df["date"].dt.day
df["month"] = df["date"].dt.month
df["dayofweek"] = df["date"].dt.dayofweek

# cyclic encoding
df["hour_sin"] = np.sin(2*np.pi*df["hour"]/24)
df["hour_cos"] = np.cos(2*np.pi*df["hour"]/24)

df["month_sin"] = np.sin(2*np.pi*df["month"]/12)
df["month_cos"] = np.cos(2*np.pi*df["month"]/12)

# -------------------------
# SEASON FEATURES
# -------------------------

print("Creating seasonal features...")

df["is_monsoon"] = df["month"].isin([6,7,8,9]).astype(int)
df["is_summer"] = df["month"].isin([3,4,5]).astype(int)
df["is_winter"] = df["month"].isin([12,1,2]).astype(int)

# -------------------------
# RAINFALL LAG FEATURES
# -------------------------

print("Creating rainfall lag features...")

df["rain_lag_1"] = df["rainfall"].shift(1)
df["rain_lag_3"] = df["rainfall"].shift(3)
df["rain_lag_6"] = df["rainfall"].shift(6)
df["rain_lag_12"] = df["rainfall"].shift(12)
df["rain_lag_24"] = df["rainfall"].shift(24)

# rainfall accumulation
df["rain_sum_6"] = df["rainfall"].rolling(6).sum()
df["rain_sum_12"] = df["rainfall"].rolling(12).sum()
df["rain_sum_24"] = df["rainfall"].rolling(24).sum()

# rainfall change
df["rain_diff"] = df["rainfall"].diff()

# -------------------------
# WEATHER INTERACTIONS
# -------------------------

print("Creating weather interaction features...")

df["temp_humidity"] = df["temperature_2m"] * df["humidity"]
df["temp_dewpoint"] = df["temperature_2m"] - df["dewpoint_2m"]

df["humidity_pressure"] = df["humidity"] * df["pressure"]

# pressure drop signal (storm indicator)
df["pressure_change"] = df["pressure"].diff()

# -------------------------
# ROLLING WEATHER FEATURES
# -------------------------

print("Creating rolling weather features...")

df["temp_roll_6"] = df["temperature_2m"].rolling(6).mean()
df["humidity_roll_6"] = df["humidity"].rolling(6).mean()
df["pressure_roll_6"] = df["pressure"].rolling(6).mean()

# -------------------------
# ASTRONOMY FEATURES
# -------------------------

print("Encoding astronomical cycles...")

df["moon_phase_sin"] = np.sin(np.radians(df["moon_phase_angle"]))
df["moon_phase_cos"] = np.cos(np.radians(df["moon_phase_angle"]))

df["sun_moon_angle"] = abs(df["sun_lon"] - df["moon_lon"])

# -------------------------
# CLEAN DATA
# -------------------------

print("Cleaning dataset...")

df = df.bfill()
df = df.ffill()

df = df.dropna()

# -------------------------
# SAVE DATASET
# -------------------------

print("Saving feature dataset...")

SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(SAVE_PATH, index=False)

print("\nFeature engineering complete")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("Dataset ready for ML training.")