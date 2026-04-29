from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "lightgbm_rainfall_model.pkl"


def load_model():
    print(f"Loading model from: {MODEL_PATH}")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"❌ Model not found at {MODEL_PATH}")

    model = joblib.load(MODEL_PATH)

    print(f"✅ Model loaded: {type(model)}")

    return model


def predict_rain(model, df):
    features = df.select_dtypes(include=["number"])
    return model.predict(features)