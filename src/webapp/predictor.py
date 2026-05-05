from pathlib import Path
import joblib
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "lightgbm_rainfall_model.pkl"


def load_model():
    print(f"Loading model from: {MODEL_PATH}")

    if not MODEL_PATH.exists():
        # Graceful fallback for cloud deployment
        st.warning(f"⚠️ Model file not found. Using fallback predictions.")
        return None  # Return None and handle in caller

    model = joblib.load(MODEL_PATH)
    print(f"✅ Model loaded: {type(model)}")
    return model


def predict_rain(model, df):
    if model is None:
        # Fallback: return zeros or simple heuristic
        features = df.select_dtypes(include=["number"])
        return [0.0] * len(features)
    
    features = df.select_dtypes(include=["number"])
    return model.predict(features)