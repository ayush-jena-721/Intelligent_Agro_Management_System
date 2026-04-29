# # # import streamlit as st
# # # import pandas as pd
# # # from datetime import datetime

# # # # Your modules
# # # from weather_fetcher import fetch_current_weather
# # # from panchang_loader import load_panchang_data, merge_with_weather
# # # from feature_builder import build_features
# # # from predictor import load_model, predict_rain
# # # from irrigation_logic import irrigation_decision

# # # # -----------------------
# # # # CONFIG
# # # # -----------------------
# # # st.set_page_config(page_title="MeghDristi", layout="wide")
# # # st.title("🌾 MeghDristi – Smart Rain & Irrigation System")

# # # # -----------------------
# # # # SIDEBAR INPUT
# # # # -----------------------
# # # st.sidebar.header("📍 User Input")

# # # lat = st.sidebar.number_input("Latitude", value=12.02)
# # # lon = st.sidebar.number_input("Longitude", value=79.56)

# # # use_current_time = st.sidebar.checkbox("Use Current Time", value=True)

# # # if use_current_time:
# # #     selected_datetime = pd.Timestamp.now()
# # # else:
# # #     date_input = st.sidebar.date_input("Select Date")
# # #     time_input = st.sidebar.time_input("Select Time")
# # #     selected_datetime = pd.Timestamp.combine(date_input, time_input)

# # # st.sidebar.markdown(f"🕒 Selected: {selected_datetime}")

# # # # -----------------------
# # # # LOAD DATA
# # # # -----------------------
# # # @st.cache_data
# # # def load_all_panchang():
# # #     p = load_panchang_data()
# # #     p["date"] = pd.to_datetime(p["date"])
# # #     return p

# # # panch = load_all_panchang()

# # # # -----------------------
# # # # FETCH WEATHER
# # # # -----------------------
# # # try:
# # #     weather = fetch_current_weather(lat, lon)
# # # except Exception as e:
# # #     st.error(f"Weather fetch failed: {e}")
# # #     st.stop()

# # # # -----------------------
# # # # FILTER PANCHANG
# # # # -----------------------
# # # panch_filtered = panch[panch["date"].dt.date == selected_datetime.date()]

# # # if panch_filtered.empty:
# # #     st.error("No Panchang data available for selected date")
# # #     st.stop()

# # # # -----------------------
# # # # MERGE DATA
# # # # -----------------------
# # # df = merge_with_weather(weather, panch_filtered)

# # # # ✅ Normalize column names (IMPORTANT FIX)
# # # df = df.rename(columns={
# # #     "precipitation_sum": "precipitation",
# # #     "rainfall": "precipitation"
# # # })

# # # # -----------------------
# # # # VALIDATE REQUIRED COLUMNS
# # # # -----------------------
# # # required_cols = ["temperature_2m", "humidity", "precipitation"]

# # # missing = [col for col in required_cols if col not in df.columns]

# # # if missing:
# # #     st.error(f"Missing columns after merge: {missing}")
# # #     st.write("Available columns:", df.columns)
# # #     st.stop()

# # # # -----------------------
# # # # BUILD FEATURES + PREDICT
# # # # -----------------------
# # # df_features = build_features(df)

# # # model = load_model()

# # # prediction = predict_rain(model, df_features)[0]
# # # decision = irrigation_decision(prediction)

# # # latest = df.iloc[-1]

# # # # -----------------------
# # # # 🟢 TOP RESULT
# # # # -----------------------
# # # st.markdown("## 🌧️ Rain Prediction")

# # # col1, col2, col3 = st.columns(3)

# # # col1.metric("Rain Today", "YES" if prediction > 0.5 else "NO")
# # # col2.metric("Rainfall (mm)", round(prediction, 2))
# # # col3.metric("Irrigation Advice", decision)

# # # # -----------------------
# # # # 🟡 CURRENT WEATHER
# # # # -----------------------
# # # st.markdown("## 🌤 Current Weather")

# # # col1, col2, col3, col4 = st.columns(4)

# # # col1.metric("🌡 Temp (°C)", round(latest.get("temperature_2m", 0), 1))
# # # col2.metric("💧 Humidity (%)", round(latest.get("humidity", 0), 1))
# # # col3.metric("🌬 Wind (km/h)", round(latest.get("wind_speed", 0), 1))
# # # col4.metric("🌧 Rain (mm)", round(latest.get("precipitation", 0), 2))

# # # # -----------------------
# # # # 🔵 PANCHANG
# # # # -----------------------
# # # st.markdown("## 🪐 Panchang Insights")

# # # col1, col2, col3, col4 = st.columns(4)

# # # col1.metric("Tithi", latest.get("tithi", "N/A"))
# # # col2.metric("Nakshatra", latest.get("nakshatra", "N/A"))
# # # col3.metric("Vara", latest.get("vara", "N/A"))
# # # col4.metric("Moon Phase", latest.get("moon_phase", "N/A"))

# # # # -----------------------
# # # # 📊 RAIN TREND
# # # # -----------------------
# # # st.markdown("## 📊 Rain Trend (Last 24 Entries)")

# # # df_plot = df.tail(24)

# # # if "date" in df_plot.columns:
# # #     chart_data = df_plot[["date", "precipitation"]].copy()
# # #     chart_data = chart_data.set_index("date")
# # #     st.line_chart(chart_data)
# # # else:
# # #     st.warning("Date column missing for plotting")

# # # # -----------------------
# # # # 📅 TABLE VIEW
# # # # -----------------------
# # # st.markdown("## 📅 Data Preview")

# # # st.dataframe(df_plot[[
# # #     "date",
# # #     "temperature_2m",
# # #     "humidity",
# # #     "precipitation"
# # # ]])

# # # import sys
# # # from pathlib import Path

# # # BASE_DIR = Path(__file__).resolve().parents[2]
# # # sys.path.append(str(BASE_DIR / "src"))
# # # import requests
# # # import streamlit as st
# # # import pandas as pd
# # # from datetime import datetime

# # # from webapp.weather_fetcher import fetch_current_weather
# # # from webapp.panchang_loader import (
# # #     load_panchang,
# # #     get_panchang_for_date,
# # #     merge_with_weather
# # # )
# # # from webapp.feature_builder import build_features
# # # from webapp.predictor import load_model, predict_rain


# # # # ---------------- UI ----------------
# # # st.set_page_config(page_title="🌧 MeghDristi Rain Predictor", layout="centered")

# # # st.title("🌧 MeghDristi - Rainfall Prediction System")
# # # st.markdown("AI + Panchang + Weather Intelligence")

# # # # ---------------- INPUT ----------------
# # # lat = st.number_input("Latitude", value=12.97)
# # # lon = st.number_input("Longitude", value=77.59)

# # # use_current_time = st.checkbox("Use current system time", value=True)

# # # if not use_current_time:
# # #     selected_date = st.datetime_input("Select Date & Time", datetime.now())
# # # else:
# # #     selected_date = datetime.now()

# # # # ---------------- RUN ----------------
# # # if st.button("Predict Rainfall"):

# # #     try:
# # #         st.info("Fetching weather data...")
# # #         weather_df = fetch_current_weather(lat, lon)

# # #         st.info("Loading Panchang...")
# # #         panch_df = load_panchang()
# # #         panch_row = get_panchang_for_date(panch_df, selected_date)

# # #         st.info("Merging data...")
# # #         final_df = merge_with_weather(weather_df, panch_row)

# # #         st.info("Building features...")
# # #         features = build_features(final_df)

# # #         st.info("Loading model...")
# # #         model = load_model()
# # #         st.write(type(model))

# # #         st.info("Predicting rainfall...")
# # #         prediction = predict_rain(model, features)

# # #         # ---------------- OUTPUT ----------------
# # #         rain_value = float(prediction[0])

# # #         st.success(f"🌧 Predicted Rainfall: {rain_value:.2f} mm")

# # #         if rain_value > 0.5:
# # #             st.warning("⚠️ Rain likely")
# # #         else:
# # #             st.info("☀️ No significant rain expected")

# # #         # Debug view (optional)
# # #         with st.expander("See Features"):
# # #             st.write(features)

# # #     except Exception as e:
# # #         st.error(f"❌ Error: {str(e)}")

# # # import sys
# # # from pathlib import Path
# # # import streamlit as st
# # # import pandas as pd
# # # from datetime import datetime

# # # # ---------------- PATH SETUP ----------------
# # # BASE_DIR = Path(__file__).resolve().parents[2]
# # # sys.path.append(str(BASE_DIR / "src"))

# # # # ---------------- IMPORTS ----------------
# # # from webapp.feature_builder import build_features, FEATURE_COLUMNS
# # # from webapp.weather_fetcher import fetch_current_weather
# # # from webapp.panchang_loader import load_panchang, get_panchang_for_date, merge_with_weather
# # # # from webapp.feature_builder import FEATURE_COLUMNS, build_features
# # # from webapp.predictor import load_model, predict_rain
# # # from webapp.panchang_mapper import map_panchang_names

# # # df = map_panchang_names(df)

# # # # ---------------- CONFIG ----------------
# # # st.set_page_config(page_title="MeghDristi", layout="wide")
# # # st.title("🌾 MeghDristi – Smart Rain & Irrigation System")

# # # CUTOFF_DATE = pd.Timestamp("2026-01-01")

# # # # ---------------- SIDEBAR ----------------
# # # st.sidebar.header("📍 User Input")

# # # lat = st.sidebar.number_input("Latitude", value=12.02)
# # # lon = st.sidebar.number_input("Longitude", value=79.56)

# # # use_current_time = st.sidebar.checkbox("Use Current Time", value=True)

# # # if use_current_time:
# # #     selected_datetime = pd.Timestamp.now()
# # # else:
# # #     date_input = st.sidebar.date_input("Select Date")
# # #     time_input = st.sidebar.time_input("Select Time")
# # #     selected_datetime = pd.Timestamp.combine(date_input, time_input)

# # # st.sidebar.markdown(f"Selected: {selected_datetime}")

# # # # ---------------- LOAD MODEL ----------------
# # # @st.cache_resource
# # # def get_model():
# # #     return load_model()

# # # model = get_model()

# # # # ---------------- LOAD HISTORICAL DATA ----------------
# # # @st.cache_data
# # # def load_historical():
# # #     df = pd.read_csv(BASE_DIR / "data/processed/weather_features.csv")
# # #     df["date"] = pd.to_datetime(df["date"])

# # #     # Normalize column names
# # #     df = df.rename(columns={
# # #         "rainfall": "precipitation",
# # #         "precipitation_sum": "precipitation"
# # #     })
# # #     df = df.loc[:, ~df.columns.duplicated()]
# # #     # st.write("Duplicate columns:", df.columns[df.columns.duplicated()])
# # #     return df

# # # hist_df = load_historical()

# # # df = hist_df.iloc[
# # #     (hist_df["date"] - selected_datetime).abs().argsort()[:1]
# # # ].copy()

# # # # ✅ Only keep model features
# # # features = df[FEATURE_COLUMNS].copy()

# # # # ---------------- MAIN BUTTON ----------------
# # # if st.button("🚀 Predict Rainfall"):

# # #     try:
# # #         # ---------------- DATA SOURCE ----------------
# # #         if selected_datetime < CUTOFF_DATE:
# # #             st.info("Using historical dataset")

# # #             df = hist_df.iloc[
# # #                 (hist_df["date"] - selected_datetime).abs().argsort()[:1]
# # #             ].copy()

# # #             use_past_context = False

# # #         else:
# # #             st.info("Using live weather + panchang")

# # #             weather = fetch_current_weather(lat, lon)

# # #             panch = load_panchang()
# # #             panch_row = get_panchang_for_date(panch, selected_datetime)

# # #             df = merge_with_weather(weather, panch_row)

# # #             use_past_context = True

# # #         # ---------------- FEATURE BUILD ----------------
# # #         # features = build_features(df, use_past_context=use_past_context)
# # #         features = build_features(df, use_past_context=True)

# # #         # ---------------- PREDICTION ----------------
# # #         # st.write("Feature count:", features.shape[1])
# # #         # st.write("Columns:", list(features.columns))
# # #         prediction = float(predict_rain(model, features)[0])

# # #         # ---------------- IRRIGATION ----------------
# # #         if prediction > 0.7:
# # #             decision = "No irrigation needed"
# # #         elif prediction > 0.3:
# # #             decision = "Light irrigation"
# # #         else:
# # #             decision = "Irrigation required"

# # #         latest = df.iloc[-1]

# # #         # ---------------- UI ----------------
# # #         st.subheader("Rain Prediction")

# # #         col1, col2, col3 = st.columns(3)
# # #         col1.metric("Rain Today", "YES" if prediction > 0.5 else "NO")
# # #         col2.metric("Rainfall (mm)", round(prediction, 2))
# # #         col3.metric("Irrigation Advice", decision)

# # #         # ---------------- WEATHER ----------------
# # #         st.subheader("Current Weather")

# # #         col1, col2, col3, col4 = st.columns(4)
# # #         col1.metric("Temp (°C)", round(latest.get("temperature_2m", 0), 1))
# # #         col2.metric("Humidity (%)", round(latest.get("humidity", 0), 1))
# # #         col3.metric("Pressure", round(latest.get("pressure", 0), 1))
# # #         col4.metric("Rain (mm)", round(latest.get("precipitation", 0), 2))

# # #         # ---------------- PANCHANG ----------------
# # #         st.subheader("Panchang")

# # #         col1, col2, col3, col4 = st.columns(4)
# # #         col1.metric("Tithi", latest.get("tithi", "N/A"))
# # #         col2.metric("Nakshatra", latest.get("nakshatra", "N/A"))
# # #         col3.metric("Vara", latest.get("vara", "N/A"))
# # #         col4.metric("Moon Phase", latest.get("moon_phase", "N/A"))

# # #         # ---------------- CHART ----------------
# # #         st.subheader("Rain Trend")

# # #         if selected_datetime < CUTOFF_DATE:
# # #             plot_df = hist_df[
# # #                 hist_df["date"].between(
# # #                     selected_datetime - pd.Timedelta(hours=24),
# # #                     selected_datetime
# # #                 )
# # #             ]
# # #         else:
# # #             plot_df = df.tail(24)

# # #         if not plot_df.empty:
# # #             st.line_chart(plot_df.set_index("date")[["precipitation"]])

# # #         # ---------------- TABLE ----------------
# # #         st.subheader("Data Preview")
# # #         st.dataframe(plot_df.tail(10))

# # #     except Exception as e:
# # #         st.error(f"Error: {e}")

# # import sys
# # from pathlib import Path
# # import streamlit as st
# # import pandas as pd
# # from datetime import datetime

# # # ---------------- PATH SETUP ----------------
# # BASE_DIR = Path(__file__).resolve().parents[2]
# # sys.path.append(str(BASE_DIR / "src"))

# # # ---------------- IMPORTS ----------------
# # from webapp.feature_builder import build_features, FEATURE_COLUMNS
# # from webapp.weather_fetcher import fetch_current_weather
# # from webapp.panchang_loader import (
# #     load_panchang,
# #     get_panchang_for_date,
# #     merge_with_weather
# # )
# # from webapp.predictor import load_model, predict_rain
# # from webapp.panchang_mapper import map_panchang_names


# # # ---------------- CONFIG ----------------
# # st.set_page_config(page_title="MeghDristi", layout="wide")
# # st.title("🌾 MeghDristi – Smart Rain & Irrigation System")

# # CUTOFF_DATE = pd.Timestamp("2026-01-01")

# # # ---------------- SIDEBAR ----------------
# # st.sidebar.header("📍 User Input")

# # lat = st.sidebar.number_input("Latitude", value=12.02)
# # lon = st.sidebar.number_input("Longitude", value=79.56)

# # use_current_time = st.sidebar.checkbox("Use Current Time", value=True)

# # if use_current_time:
# #     selected_datetime = pd.Timestamp.now()
# # else:
# #     date_input = st.sidebar.date_input("Select Date")
# #     time_input = st.sidebar.time_input("Select Time")
# #     selected_datetime = pd.Timestamp.combine(date_input, time_input)

# # st.sidebar.markdown(f"🕒 Selected: {selected_datetime}")

# # # ---------------- LOAD MODEL ----------------
# # @st.cache_resource
# # def get_model():
# #     return load_model()

# # model = get_model()

# # # ---------------- LOAD HISTORICAL DATA ----------------
# # @st.cache_data
# # def load_historical():
# #     df = pd.read_csv(BASE_DIR / "data/processed/weather_features.csv")

# #     # ✅ Fix date
# #     df["date"] = pd.to_datetime(df["date"], errors="coerce")

# #     # ✅ Normalize column names
# #     df = df.rename(columns={
# #         "rainfall": "precipitation",
# #         "precipitation_sum": "precipitation"
# #     })

# #     # ✅ REMOVE duplicate columns (CRITICAL FIX)
# #     df = df.loc[:, ~df.columns.duplicated()].copy()

# #     # ✅ RESET index (fix reindex error)
# #     df = df.reset_index(drop=True)

# #     return df

# # hist_df = load_historical()

# # # ---------------- SAFE ROW PICKER ----------------
# # def get_nearest_row(df, selected_datetime):
# #     df = df.copy()

# #     # Ensure sorted + unique index
# #     df = df.sort_values("date").drop_duplicates(subset=["date"])
# #     df = df.reset_index(drop=True)

# #     idx = (df["date"] - selected_datetime).abs().idxmin()

# #     return df.loc[[idx]].copy()

# # # ---------------- MAIN BUTTON ----------------
# # if st.button("🚀 Predict Rainfall"):

# #     try:
# #         # ---------------- DATA SOURCE ----------------
# #         if selected_datetime < CUTOFF_DATE:
# #             st.info("Using historical dataset")

# #             df = get_nearest_row(hist_df, selected_datetime)
# #             use_past_context = False

# #         else:
# #             st.info("Using live weather + panchang")

# #             weather = fetch_current_weather(lat, lon)

# #             panch = load_panchang()
# #             panch_row = get_panchang_for_date(panch, selected_datetime)

# #             df = merge_with_weather(weather, panch_row)

# #             # ✅ CLEAN AFTER MERGE (IMPORTANT)
# #             df = df.loc[:, ~df.columns.duplicated()].copy()
# #             df = df.reset_index(drop=True)

# #             use_past_context = True

# #         # ---------------- MAP PANCHANG ----------------
# #         df = map_panchang_names(df)
        

# #         # ---------------- FEATURE BUILD ----------------
# #         features = build_features(df, use_past_context=use_past_context)

# #         # ✅ FORCE FEATURE ALIGNMENT (MODEL SAFE)
# #         features = features.reindex(columns=FEATURE_COLUMNS, fill_value=0)

# #         # ---------------- PREDICTION ----------------
# #         prediction = float(predict_rain(model, features)[0])

# #         # ---------------- IRRIGATION ----------------
# #         if prediction > 0.7:
# #             decision = "No irrigation needed"
# #         elif prediction > 0.3:
# #             decision = "Light irrigation"
# #         else:
# #             decision = "Irrigation required"

# #         latest = df.iloc[-1]

# #         # ---------------- UI ----------------
# #         st.subheader("🌧 Rain Prediction")

# #         col1, col2, col3 = st.columns(3)
# #         col1.metric("Rain Today", "YES" if prediction > 0.5 else "NO")
# #         col2.metric("Rainfall (mm)", round(prediction, 2))
# #         col3.metric("Irrigation Advice", decision)

# #         # ---------------- WEATHER ----------------
# #         st.subheader("🌤 Current Weather")

# #         col1, col2, col3, col4 = st.columns(4)
# #         col1.metric("Temp (°C)", round(latest.get("temperature_2m", 0), 1))
# #         col2.metric("Humidity (%)", round(latest.get("humidity", 0), 1))
# #         col3.metric("Pressure", round(latest.get("pressure", 0), 1))
# #         col4.metric("Rain (mm)", round(latest.get("precipitation", 0), 2))

# #         # ---------------- PANCHANG ----------------
# #         st.subheader("🪐 Panchang")

# #         col1, col2, col3, col4 = st.columns(4)
# #         col1.metric("Tithi", latest.get("tithi", "N/A"))
# #         col2.metric("Nakshatra", latest.get("nakshatra", "N/A"))
# #         col3.metric("Vara", latest.get("vara", "N/A"))
# #         col4.metric("Moon Phase", latest.get("moon_phase", "N/A"))

# #         # ---------------- CHART ----------------
# #         st.subheader("📊 Rain Trend")

# #         if selected_datetime < CUTOFF_DATE:
# #             plot_df = hist_df[
# #                 hist_df["date"].between(
# #                     selected_datetime - pd.Timedelta(hours=24),
# #                     selected_datetime
# #                 )
# #             ]
# #         else:
# #             plot_df = df.tail(24)

# #         if not plot_df.empty:
# #             plot_df = plot_df.drop_duplicates(subset=["date"])
# #             st.line_chart(plot_df.set_index("date")[["precipitation"]])

# #         # ---------------- TABLE ----------------
# #         st.subheader("📅 Data Preview")
# #         st.dataframe(plot_df.tail(10))

# #     except Exception as e:
# #         st.error(f"❌ Error: {e}")
# import sys
# from pathlib import Path
# import streamlit as st
# import pandas as pd
# from datetime import datetime

# # ---------------- PATH SETUP ----------------
# BASE_DIR = Path(__file__).resolve().parents[2]
# sys.path.append(str(BASE_DIR / "src"))

# # ---------------- IMPORTS ----------------
# from webapp.feature_builder import build_features, FEATURE_COLUMNS
# from webapp.weather_fetcher import fetch_current_weather
# from webapp.panchang_loader import load_panchang, get_panchang_for_date, merge_with_weather
# from webapp.predictor import load_model, predict_rain
# from webapp.panchang_mapper import map_panchang_names

# # ---------------- CONFIG ----------------
# st.set_page_config(page_title="MeghDristi", layout="wide")
# st.title("🌾 MeghDristi – Smart Rain & Irrigation System")

# CUTOFF_DATE = pd.Timestamp("2026-01-01")

# # ---------------- SIDEBAR ----------------
# st.sidebar.header("📍 User Input")

# lat = st.sidebar.number_input("Latitude", value=12.02)
# lon = st.sidebar.number_input("Longitude", value=79.56)
# use_current_time = st.sidebar.checkbox("Use Current Time", value=True)

# if use_current_time:
#     selected_datetime = pd.Timestamp.now()
# else:
#     date_input = st.sidebar.date_input("Select Date")
#     time_input = st.sidebar.time_input("Select Time")
#     selected_datetime = pd.Timestamp.combine(date_input, time_input)

# st.sidebar.markdown(f"🕒 Selected: {selected_datetime}")

# # ---------------- LOAD MODEL ----------------
# @st.cache_resource
# def get_model():
#     return load_model()

# model = get_model()

# # ---------------- LOAD HISTORICAL WEATHER ----------------
# @st.cache_data
# def load_historical():
#     df = pd.read_csv(BASE_DIR / "data/processed/weather_features.csv")
#     df["date"] = pd.to_datetime(df["date"], errors="coerce")
#     df = df.rename(columns={"rainfall": "precipitation", "precipitation_sum": "precipitation"})
#     df = df.loc[:, ~df.columns.duplicated()].copy()
#     df = df.reset_index(drop=True)
#     return df

# hist_df = load_historical()

# # ---------------- SAFE ROW PICKER ----------------
# def get_nearest_row(df, selected_datetime):
#     df = df.copy()
#     df = df.sort_values("date").drop_duplicates(subset=["date"]).reset_index(drop=True)
#     idx = (df["date"] - selected_datetime).abs().idxmin()
#     return df.loc[[idx]].copy()

# # ---------------- MAIN BUTTON ----------------
# if st.button("🚀 Predict Rainfall"):

#     try:
#         if selected_datetime < CUTOFF_DATE:
#             st.info("Using historical dataset + Panchang")
#             # ---------------- HISTORICAL WEATHER ----------------
#             df = get_nearest_row(hist_df, selected_datetime)
            
#             # ---------------- HISTORICAL PANCHANG ----------------
#             panch = load_panchang()
#             panch_row = get_panchang_for_date(panch, selected_datetime)

#             df = merge_with_weather(df, panch_row)
#             df = df.loc[:, ~df.columns.duplicated()].copy().reset_index(drop=True)
#             use_past_context = False

#         else:
#             st.info("Using live weather + Panchang")
#             weather = fetch_current_weather(lat, lon)
#             panch = load_panchang()
#             panch_row = get_panchang_for_date(panch, selected_datetime)
#             df = merge_with_weather(weather, panch_row)
#             df = df.loc[:, ~df.columns.duplicated()].copy().reset_index(drop=True)
#             use_past_context = True

#         # ---------------- MAP PANCHANG ----------------
#         df = map_panchang_names(df)
#         for col in ["tithi", "nakshatra", "vara"]:
#             df[col] = df.get(col, "Unknown").fillna("Unknown")

#         # ---------------- FEATURE BUILD ----------------
#         features = build_features(df, use_past_context=use_past_context)
#         features = features.reindex(columns=FEATURE_COLUMNS, fill_value=0)

#         # ---------------- PREDICTION ----------------
#         prediction = float(predict_rain(model, features)[0])

#         # ---------------- IRRIGATION ----------------
#         if prediction > 0.7:
#             decision = "No irrigation needed"
#         elif prediction > 0.3:
#             decision = "Light irrigation"
#         else:
#             decision = "Irrigation required"

#         latest = df.iloc[-1]

#         # ---------------- UI ----------------
#         st.subheader("🌧 Rain Prediction")
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Rain Today", "YES" if prediction > 0.5 else "NO")
#         col2.metric("Rainfall (mm)", round(prediction, 2))
#         col3.metric("Irrigation Advice", decision)

#         st.subheader("🌤 Current Weather")
#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("Temp (°C)", round(latest.get("temperature_2m", 0), 1))
#         col2.metric("Humidity (%)", round(latest.get("humidity", 0), 1))
#         col3.metric("Pressure", round(latest.get("pressure", 0), 1))
#         col4.metric("Rain (mm)", round(latest.get("precipitation", 0), 2))

#         st.subheader("🪐 Panchang")
#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("Tithi", latest.get("tithi", "Unknown"))
#         col2.metric("Nakshatra", latest.get("nakshatra", "Unknown"))
#         col3.metric("Vara", latest.get("vara", "Unknown"))
#         col4.metric("Moon Phase", latest.get("moon_phase", "Unknown"))

#         st.subheader("📊 Rain Trend")
#         if selected_datetime < CUTOFF_DATE:
#             plot_df = hist_df[
#                 hist_df["date"].between(selected_datetime - pd.Timedelta(hours=24), selected_datetime)
#             ]
#         else:
#             plot_df = df.tail(24)

#         if not plot_df.empty:
#             plot_df = plot_df.drop_duplicates(subset=["date"])
#             st.line_chart(plot_df.set_index("date")[["precipitation"]])

#         st.subheader("📅 Data Preview")
#         st.dataframe(plot_df.tail(10))

#     except Exception as e:
#         st.error(f"❌ Error: {e}")

import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# ---------------- PATH SETUP ----------------
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR / "src"))

# ---------------- IMPORTS ----------------
from webapp.feature_builder import build_features, FEATURE_COLUMNS
from webapp.weather_fetcher import fetch_current_weather
from webapp.panchang_loader import load_panchang, get_panchang_for_date, merge_with_weather
from webapp.predictor import load_model, predict_rain
from webapp.panchang_mapper import map_panchang_names

# ---------------- CONFIG ----------------
st.set_page_config(page_title="MeghDristi", layout="wide")

# ---------------- GLASS UI ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.glass {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(14px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    color: white;
}

.title {
    font-size: 20px;
    opacity: 0.8;
}

.value {
    font-size: 32px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🌾 MeghDristi – Smart Rain & Irrigation System")

CUTOFF_DATE = pd.Timestamp("2026-01-01")

# ---------------- SIDEBAR ----------------
st.sidebar.header("📍 User Input")

lat = st.sidebar.number_input("Latitude", value=12.02)
lon = st.sidebar.number_input("Longitude", value=79.56)
use_current_time = st.sidebar.checkbox("Use Current Time", value=True)

if use_current_time:
    selected_datetime = pd.Timestamp.now()
else:
    date_input = st.sidebar.date_input("Select Date")
    time_input = st.sidebar.time_input("Select Time")
    selected_datetime = pd.Timestamp.combine(date_input, time_input)

# ---------------- MODEL ----------------
@st.cache_resource
def get_model():
    return load_model()

model = get_model()

# ---------------- HISTORICAL ----------------
@st.cache_data
def load_historical():
    df = pd.read_csv(BASE_DIR / "data/processed/weather_features.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.rename(columns={"rainfall": "precipitation"})
    return df

hist_df = load_historical()

def get_nearest_row(df, selected_datetime):
    df = df.sort_values("date").drop_duplicates("date")
    idx = (df["date"] - selected_datetime).abs().idxmin()
    return df.loc[[idx]].copy()

# ---------------- FUTURE PRED ----------------
def predict_next_days(model, base_df, days=5):
    future = []
    temp = base_df.copy()

    for _ in range(days):
        temp["date"] += pd.Timedelta(days=1)

        features = build_features(temp, True)
        features = features.reindex(columns=FEATURE_COLUMNS, fill_value=0)

        pred = float(predict_rain(model, features)[0])
        pred = max(0, pred)

        future.append({"date": temp["date"].iloc[-1], "rain": pred})
        temp["precipitation"] = pred

    return pd.DataFrame(future)

# ---------------- ADVISORY ----------------
def generate_advisory(temp, humidity, rain):
    if rain > 0.7:
        return "🚫 Avoid spraying. Ensure drainage."
    elif rain > 0.3:
        return "🌱 Good for sowing."
    elif temp > 35:
        return "🔥 Increase irrigation."
    elif humidity < 30:
        return "🌾 Mulching recommended."
    return "✅ Conditions stable."

# ---------------- MAIN ----------------
if st.button("🚀 Predict"):

    try:
        # ---------- DATA ----------
        if selected_datetime < CUTOFF_DATE:
            df = get_nearest_row(hist_df, selected_datetime)
        else:
            df = fetch_current_weather(lat, lon)

        panch = load_panchang()
        panch_row = get_panchang_for_date(panch, selected_datetime)

        df = merge_with_weather(df, panch_row)
        df = map_panchang_names(df)

        latest = df.iloc[-1]

        # ---------- PRED ----------
        features = build_features(df, True)
        features = features.reindex(columns=FEATURE_COLUMNS, fill_value=0)

        prediction = float(predict_rain(model, features)[0])
        prediction = max(0, prediction)

        # ---------- IRRIGATION ----------
        soil = latest.get("humidity", 50)

        if prediction > 0.7:
            decision = "🚫 Skip irrigation"
        elif prediction > 0.3:
            decision = "💧 Light irrigation"
        elif soil < 40:
            decision = "🚿 Immediate irrigation"
        else:
            decision = "🌱 Normal watering"

        advisory = generate_advisory(
            latest.get("temperature_2m", 0),
            latest.get("humidity", 0),
            prediction
        )

        # ---------- CARDS ----------
        col1, col2, col3 = st.columns(3)

        col1.markdown(f'<div class="glass"><div class="title">Rain</div><div class="value">{prediction:.2f}</div></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="glass"><div class="title">Temp</div><div class="value">{latest.get("temperature_2m",0):.1f}°C</div></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="glass"><div class="title">Humidity</div><div class="value">{latest.get("humidity",0):.1f}%</div></div>', unsafe_allow_html=True)

        # ---------- DECISION ----------
        col1, col2 = st.columns(2)

        col1.markdown(f'<div class="glass"><h3>🚿 Irrigation</h3><p>{decision}</p></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="glass"><h3>🌾 Advisory</h3><p>{advisory}</p></div>', unsafe_allow_html=True)

        # ---------- FUTURE ----------
        future_df = predict_next_days(model, df.tail(1))

        st.markdown("### 📈 Rain Forecast")
        st.line_chart(future_df.set_index("date"))

        # ---------- INSIGHT GRAPH ----------
        st.markdown("### 💧 Rain vs Humidity")
        if "humidity" in df.columns:
            st.line_chart(df.set_index("date")[["humidity", "precipitation"]])

        # ---------- TREND ----------
        future_df["trend"] = future_df["rain"].diff()

        st.markdown("### ⚖️ Rain Trend")
        st.bar_chart(future_df.set_index("date")["trend"])

        # ---------- PANCHANG ----------
        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(f'<div class="glass">Tithi<br>{latest.get("tithi","")}</div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="glass">Nakshatra<br>{latest.get("nakshatra","")}</div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="glass">Vara<br>{latest.get("vara","")}</div>', unsafe_allow_html=True)
        col4.markdown(f'<div class="glass">Moon<br>{latest.get("moon_phase","")}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")