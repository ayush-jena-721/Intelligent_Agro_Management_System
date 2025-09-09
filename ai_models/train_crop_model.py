import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os 

# 1. Load dataset
data = pd.read_csv("/home/stemland/Documents/agri_scense/sdml23-project12/datasets/Crop_recommendation.csv")

# 2. Split features (X) and target (y)
X = data.drop("label", axis=1)
y = data["label"]

# 3. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 5. Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# 6. Save model
joblib.dump(model, "crop_model.pkl", compress=3)
print("Model saved at ai_models/crop_model.pkl")



