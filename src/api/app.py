# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# # Import your existing engine
# from src.predict.predict_engine import generate_forecast

# app = FastAPI(title="MeghDristi Weather API 🌧")

# # Allow frontend access (important for dashboard)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------------------------------------
# # ROOT
# # ---------------------------------------
# @app.get("/")
# def home():
#     return {
#         "message": "MeghDristi API is running 🚀"
#     }


# # ---------------------------------------
# # FORECAST ENDPOINT
# # ---------------------------------------
# @app.get("/forecast")
# def forecast():
#     try:
#         result = generate_forecast()

#         return {
#             "status": "success",
#             "data": result
#         }

#     except Exception as e:
#         return {
#             "status": "error",
#             "message": str(e)
#         }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from src.predict.predict_engine import generate_forecast

app = FastAPI(title="MeghDristi Weather API 🌧")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API running 🚀"}


@app.get("/forecast")
def forecast_api():
    try:
        # TEMP: using last row from dataset
        df = pd.read_csv("data/processed/weather_features.csv")
        latest_row = df.iloc[-1]

        features_df = pd.DataFrame([latest_row])

        result = generate_forecast(features_df)

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }