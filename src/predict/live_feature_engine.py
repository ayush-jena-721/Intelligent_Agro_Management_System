# import requests
# import pandas as pd
# import numpy as np
# from datetime import datetime
# import joblib

# MODEL_PATH = "models/lightgbm_rainfall_model.pkl"
# model = joblib.load(MODEL_PATH)

# LAT = 12.02
# LON = 79.56


# # ---------------------------------------
# # FETCH FUTURE WEATHER
# # ---------------------------------------

# def fetch_future_weather():

#     url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,surface_pressure,precipitation&forecast_days=7&timezone=auto"

#     data = requests.get(url).json()

#     df = pd.DataFrame(data["hourly"])
#     df["time"] = pd.to_datetime(df["time"])

#     return df


# # ---------------------------------------
# # PANCHANGAM (DYNAMIC)
# # ---------------------------------------

# def add_panchangam(df):

#     from skyfield.api import load

#     ts = load.timescale()
#     eph = load('de440s.bsp')

#     earth = eph['earth']
#     moon = eph['moon']
#     sun = eph['sun']

#     moon_angles = []

#     for t in df["time"]:
#         tt = ts.from_datetime(t.to_pydatetime())

#         moon_pos = earth.at(tt).observe(moon).apparent()
#         angle = moon_pos.phase_angle().degrees

#         moon_angles.append(angle)

#     df["moon_phase_angle"] = moon_angles
#     df["tithi_index"] = (df["moon_phase_angle"] // 12 + 1).astype(int)

#     return df


# # ---------------------------------------
# # FEATURE ENGINEERING (CRITICAL)
# # ---------------------------------------

# def build_features(df):

#     df["hour"] = df["time"].dt.hour
#     df["month"] = df["time"].dt.month

#     df["hour_sin"] = np.sin(2*np.pi*df["hour"]/24)
#     df["hour_cos"] = np.cos(2*np.pi*df["hour"]/24)

#     df["month_sin"] = np.sin(2*np.pi*df["month"]/12)
#     df["month_cos"] = np.cos(2*np.pi*df["month"]/12)

#     df.rename(columns={
#         "relativehumidity_2m": "humidity",
#         "surface_pressure": "pressure"
#     }, inplace=True)

#     return df


# # ---------------------------------------
# # FEATURE ALIGNMENT
# # ---------------------------------------

# def align_features(df):

#     required = model.feature_name_

#     for col in required:
#         if col not in df.columns:
#             df[col] = 0

#     return df[required]


# # ---------------------------------------
# # FINAL FORECAST ENGINE
# # ---------------------------------------

# def generate_forecast():

#     df = fetch_future_weather()

#     df = add_panchangam(df)

#     df = build_features(df)

#     daily = []

#     # Group by date (take mean of day)
#     df["date"] = df["time"].dt.date

#     grouped = df.groupby("date").mean().reset_index()

#     for i, row in grouped.iterrows():

#         X = align_features(pd.DataFrame([row]))

#         pred = model.predict(X)[0]
#         pred = max(0, round(float(pred), 2))

#         daily.append({
#             "date": str(row["date"]),
#             "rainfall_mm": pred
#         })

#     return daily