import joblib

model = joblib.load("models/lightgbm_rainfall_model.pkl")

print("Total features:", model.n_features_in_)
print(type(model))
# THIS IS GOLD 👇
print(model.feature_name_)

