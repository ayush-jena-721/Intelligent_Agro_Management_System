# ==========================================
# HYBRID LSTM RAINFALL PREDICTION SYSTEM
# (Weather + Panchang Features)
# ==========================================

import numpy as np
import pandas as pd
import joblib
import os

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout

# ==========================================
# CONFIG
# ==========================================
DATA_PATH = "data/processed/weather_features.csv"

SEQ_LENGTH = 30
EPOCHS = 25
BATCH_SIZE = 32

MODEL_PATH = "models/lstm_hybrid.h5"
SCALER_PATH = "models/lstm_scaler.save"

os.makedirs("models", exist_ok=True)

# ==========================================
# FEATURES (CURATED)
# ==========================================
FEATURES = [
    "precipitation",  # TARGET (must be first)

    # weather
    "temperature_2m",
    "humidity",
    "pressure",
    "dewpoint_2m",

    # astro
    "tithi_index",
    "nakshatra_index",
    "yoga_index",
    "moon_phase_sin",
    "moon_phase_cos",
    "sun_moon_angle",

    # time
    "month_sin",
    "month_cos",
    "dayofweek",
    "is_monsoon",

    # rain memory
    "rain_lag_1",
    "rain_lag_3",
    "rain_sum_6",
    "rain_sum_12"
]

# ==========================================
# LOAD DATA
# ==========================================
def load_data():
    df = pd.read_csv(DATA_PATH)

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    df = df[FEATURES]

    # Fill missing safely
    df = df.fillna(method="ffill").fillna(0)

    return df


# ==========================================
# SCALE DATA
# ==========================================
def scale_data(df):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df)

    joblib.dump(scaler, SCALER_PATH)

    return scaled, scaler


# ==========================================
# CREATE SEQUENCES
# ==========================================
def create_sequences(data, seq_length):
    X, y = [], []

    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length][0])  # precipitation

    return np.array(X), np.array(y)


# ==========================================
# BUILD MODEL
# ==========================================
def build_model(input_shape):
    model = Sequential()

    model.add(LSTM(128, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))

    model.add(LSTM(64))
    model.add(Dropout(0.2))

    model.add(Dense(32, activation="relu"))
    model.add(Dense(1))  # output rainfall

    model.compile(
        optimizer="adam",
        loss="mse",
        metrics=["mae"]
    )

    return model


# ==========================================
# TRAIN MODEL
# ==========================================
def train_model(df):
    scaled_data, scaler = scale_data(df)

    X, y = create_sequences(scaled_data, SEQ_LENGTH)

    print("📊 Training Data Shape:", X.shape, y.shape)

    model = build_model((X.shape[1], X.shape[2]))

    model.fit(
        X, y,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=0.2,
        verbose=1
    )

    model.save(MODEL_PATH)

    print("✅ Model saved at:", MODEL_PATH)

    return model, scaler


# ==========================================
# FORECAST FUTURE DAYS
# ==========================================
def forecast_future(model, scaler, df, days=7):
    last_data = df.tail(SEQ_LENGTH).values
    last_scaled = scaler.transform(last_data)

    current_seq = last_scaled.copy()
    predictions = []

    for _ in range(days):
        input_seq = current_seq.reshape(1, SEQ_LENGTH, current_seq.shape[1])

        pred_scaled = model.predict(input_seq, verbose=0)[0][0]

        predictions.append(pred_scaled)

        # update next step
        next_row = current_seq[-1].copy()
        next_row[0] = pred_scaled  # update precipitation only

        current_seq = np.vstack([current_seq[1:], next_row])

    # inverse scaling
    dummy = np.zeros((len(predictions), current_seq.shape[1]))
    dummy[:, 0] = predictions

    inv = scaler.inverse_transform(dummy)

    return inv[:, 0]


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":

    print("🚀 Loading data...")
    df = load_data()

    print("📊 Sample Data:")
    print(df.head())

    print("\n🧠 Training LSTM...")
    model, scaler = train_model(df)

    print("\n🌧️ Predicting next 7 days...")
    future = forecast_future(model, scaler, df, days=7)

    print("\n📅 Future Rainfall Prediction:")
    for i, val in enumerate(future):
        print(f"Day {i+1}: {val:.2f} mm")