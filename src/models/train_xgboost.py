# # src/models/train_xgboost.py (XGBoost 3.x compatible)
# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# import xgboost as xgb
# import matplotlib.pyplot as plt
# import os

# print(f"XGBoost version: {xgb.__version__}")

# # -------------------------
# # 1. Load dataset
# # -------------------------
# print("Loading feature dataset...")
# df = pd.read_csv("data/processed/feature_dataset.csv")
# df["date"] = pd.to_datetime(df["date"])

# # -------------------------
# # 2. Define features and target
# # -------------------------
# target = "rainfall"
# exclude_cols = ["date"]
# features = [col for col in df.columns if col not in exclude_cols + [target]]

# X = df[features]
# y = df[target]

# # -------------------------
# # 3. Train/Test/Validation split
# # -------------------------
# print("Splitting dataset...")
# X_train_full, X_test, y_train_full, y_test = train_test_split(
#     X, y, test_size=0.2, shuffle=False
# )
# X_train, X_val, y_train, y_val = train_test_split(
#     X_train_full, y_train_full, test_size=0.25, shuffle=False
# )

# print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

# # -------------------------
# # 4. Train XGBoost Regressor (XGBoost 3.x compatible)
# # -------------------------
# print("Training XGBoost model...")

# # Parse version
# version_parts = xgb.__version__.split(".")
# major_version = int(version_parts[0])
# minor_version = int(version_parts[1]) if len(version_parts) > 1 else 0

# # XGBoost 3.x: early_stopping_rounds goes in constructor, not fit()
# if major_version >= 2:
#     # XGBoost 2.0+ and 3.x: early_stopping_rounds is a constructor parameter
#     model = xgb.XGBRegressor(
#         n_estimators=1000,
#         learning_rate=0.05,
#         max_depth=6,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         random_state=42,
#         early_stopping_rounds=50  # Moved to constructor in 2.0+
#     )
    
#     fit_kwargs = {
#         "eval_set": [(X_val, y_val)],
#         "verbose": 50
#     }
    
# else:
#     # XGBoost 1.x: early_stopping_rounds in fit()
#     model = xgb.XGBRegressor(
#         n_estimators=1000,
#         learning_rate=0.05,
#         max_depth=6,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         random_state=42
#     )
    
#     if minor_version >= 7:
#         fit_kwargs = {
#             "eval_set": [(X_val, y_val)],
#             "early_stopping_rounds": 50,
#             "verbose": 50
#         }
#     else:
#         print("Older XGBoost detected: skipping early stopping and eval_set")
#         fit_kwargs = {}

# model.fit(X_train, y_train, **fit_kwargs)

# # -------------------------
# # 5. Predictions and evaluation
# # -------------------------
# print("Evaluating model...")
# y_pred = model.predict(X_test)

# mae = mean_absolute_error(y_test, y_pred)
# rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# r2 = r2_score(y_test, y_pred)

# print(f"MAE: {mae:.4f}")
# print(f"RMSE: {rmse:.4f}")
# print(f"R²: {r2:.4f}")

# # Print best iteration if early stopping was used
# if hasattr(model, 'best_iteration') and model.best_iteration:
#     print(f"Best iteration: {model.best_iteration}")

# # -------------------------
# # 6. Feature importance
# # -------------------------
# print("Plotting feature importance...")
# xgb.plot_importance(model, max_num_features=15, importance_type='gain', height=0.5)
# plt.tight_layout()
# plt.show()

# # -------------------------
# # 7. Save model
# # -------------------------
# print("Saving model...")
# os.makedirs("models", exist_ok=True)
# model.save_model("models/xgboost_rainfall_model.json")

# print("Training complete!")

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import xgboost as xgb
import lightgbm as lgb


# -------------------------
# 1. Load dataset
# -------------------------
print("Loading dataset...")

df = pd.read_csv("data/processed/weather_features.csv")
df["date"] = pd.to_datetime(df["date"])

target = "rainfall"
exclude_cols = ["date"]

features = [c for c in df.columns if c not in exclude_cols + [target]]

X = df[features]
y = df[target]

# -----------------------------
# Drop unused columns
# -----------------------------

drop_cols = ["date", "rainfall", "hour", "hour_sin", "hour_cos"]

X = df.drop(columns=drop_cols)
y = df["rainfall"]

# -------------------------
# 2. Time-based split
# -------------------------

print("Splitting dataset...")

X_train_full, X_test, y_train_full, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, y_train_full, test_size=0.25, shuffle=False
)

print("Train:", len(X_train))
print("Val:", len(X_val))
print("Test:", len(X_test))


# -------------------------
# 3. XGBoost Tuned Model
# -------------------------

print("\nTraining tuned XGBoost...")

xgb_model = xgb.XGBRegressor(

    n_estimators=2000,
    learning_rate=0.03,
    max_depth=8,
    min_child_weight=3,

    subsample=0.85,
    colsample_bytree=0.85,

    gamma=0.1,
    reg_alpha=0.1,
    reg_lambda=1.0,

    random_state=42,
    early_stopping_rounds=50
)

xgb_model.fit(
    X_train,
    y_train,
    eval_set=[(X_val, y_val)],
    verbose=50
)


# -------------------------
# Evaluate XGBoost
# -------------------------

y_pred_xgb = xgb_model.predict(X_test)

mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
rmse_xgb = np.sqrt(mean_squared_error(y_test, y_pred_xgb))
r2_xgb = r2_score(y_test, y_pred_xgb)

print("\nXGBOOST RESULTS")
print("MAE :", mae_xgb)
print("RMSE:", rmse_xgb)
print("R2  :", r2_xgb)


# -------------------------
# 4. LightGBM Model
# -------------------------

print("\nTraining LightGBM...")

lgb_model = lgb.LGBMRegressor(

    n_estimators=2000,
    learning_rate=0.03,

    max_depth=8,
    num_leaves=40,

    subsample=0.85,
    colsample_bytree=0.85,

    random_state=42
)

lgb_model.fit(
    X_train,
    y_train,
    eval_set=[(X_val, y_val)],
    eval_metric="rmse",
    callbacks=[lgb.early_stopping(50)]
)


# -------------------------
# Evaluate LightGBM
# -------------------------

y_pred_lgb = lgb_model.predict(X_test)

mae_lgb = mean_absolute_error(y_test, y_pred_lgb)
rmse_lgb = np.sqrt(mean_squared_error(y_test, y_pred_lgb))
r2_lgb = r2_score(y_test, y_pred_lgb)

print("\nLIGHTGBM RESULTS")
print("MAE :", mae_lgb)
print("RMSE:", rmse_lgb)
print("R2  :", r2_lgb)


# -------------------------
# 5. Save Feature Importance
# -------------------------

print("\nSaving feature importance...")

importance = xgb_model.get_booster().get_score(importance_type="gain")

imp_df = pd.DataFrame({
    "feature": list(importance.keys()),
    "importance": list(importance.values())
}).sort_values("importance", ascending=False)

os.makedirs("models", exist_ok=True)

imp_df.to_csv("models/feature_importance.csv", index=False)


# -------------------------
# 6. Plot Feature Importance
# -------------------------

plt.figure(figsize=(8,6))

top_features = imp_df.head(15)

plt.barh(top_features["feature"], top_features["importance"])

plt.title("Top Feature Importance")
plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()


# -------------------------
# 7. Save models
# -------------------------

print("\nSaving models...")

xgb_model.save_model("models/xgboost_rainfall_model.json")

import joblib
joblib.dump(lgb_model, "models/lightgbm_rainfall_model.pkl")

print("\nTraining complete!")