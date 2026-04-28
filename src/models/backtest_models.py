import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("\n====== MEGHDRISTI BACKTEST ENGINE ======\n")

# -----------------------------
# Load dataset
# -----------------------------

df = pd.read_csv("data/processed/weather_features.csv")

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

print("Dataset Loaded:", df.shape)


# -----------------------------
# Drop non-usable columns
# -----------------------------

drop_cols = ["date","rainfall","hour","hour_sin","hour_cos"]
X = df.drop(columns=drop_cols)
y = df["rainfall"]


# -----------------------------
# Time-based split
# -----------------------------

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\nTrain Size:", X_train.shape)
print("Test Size :", X_test.shape)


# -----------------------------
# Load trained models
# -----------------------------

print("\nLoading models...")

# Load XGBoost model
xgb_model = xgb.XGBRegressor()
xgb_model.load_model("models/xgboost_rainfall_model.json")

# Load LightGBM model
lgb_model = joblib.load("models/lightgbm_rainfall_model.pkl")

print("\nModels loaded successfully")


# -----------------------------
# Predictions
# -----------------------------

xgb_pred = xgb_model.predict(X_test)
lgb_pred = lgb_model.predict(X_test)


# -----------------------------
# Evaluation Function
# -----------------------------

def evaluate(y_true, y_pred, name):

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    print(f"\n{name} RESULTS")
    print("MAE :", round(mae,3))
    print("RMSE:", round(rmse,3))
    print("R2  :", round(r2,3))


# -----------------------------
# Evaluate models
# -----------------------------

evaluate(y_test, xgb_pred, "XGBoost")
evaluate(y_test, lgb_pred, "LightGBM")


# -----------------------------
# Save prediction comparison
# -----------------------------

results = pd.DataFrame({
    "actual_rainfall": y_test,
    "xgb_prediction": xgb_pred,
    "lgb_prediction": lgb_pred
})

results.to_csv("models/backtest_results.csv", index=False)

print("\nBacktest predictions saved")

print("\n====== BACKTEST COMPLETE ======\n")