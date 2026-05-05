import pandas as pd
import numpy as np
from pathlib import Path

print("\n====== MEGHDRISTI MODEL VERIFICATION ======\n")

DATA_PATH = Path("data/processed/weather_features.csv")

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
print("\nColumns:\n", df.columns.tolist())


# -----------------------------
# 1. CHECK TARGET LEAKAGE
# -----------------------------
print("\n--- Checking Target Leakage ---")

target = "rainfall"

# keep only numeric columns
numeric_df = df.select_dtypes(include=[np.number])

leakage_features = []

for col in numeric_df.columns:
    if col != target:
        corr = numeric_df[col].corr(numeric_df[target])
        if abs(corr) > 0.95:
            leakage_features.append((col, corr))

if leakage_features:
    print("⚠️ Possible leakage features:")
    for f in leakage_features:
        print(f)
else:
    print("No obvious leakage detected")


# -----------------------------
# 2. CHECK FUTURE DATA USAGE
# -----------------------------

print("\n--- Checking Future Leakage ---")

future_keywords = ["lead", "future", "t+"]

future_cols = []

for col in df.columns:
    if any(k in col.lower() for k in future_keywords):
        future_cols.append(col)

if future_cols:
    print("⚠️ Future-looking columns found:")
    print(future_cols)
else:
    print("No future feature names detected")


# -----------------------------
# 3. CHECK RAINFALL FEATURES
# -----------------------------

print("\n--- Checking Rainfall Feature Usage ---")

rain_features = [c for c in df.columns if "rain" in c.lower()]

print("Rain-related features:")
print(rain_features)


# -----------------------------
# 4. CHECK DATA ORDER
# -----------------------------

print("\n--- Checking Time Order ---")

if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])
    ordered = df["date"].is_monotonic_increasing

    if ordered:
        print("Dataset correctly ordered by time")
    else:
        print("⚠️ Dataset NOT time ordered")
else:
    print("No date column found")


# -----------------------------
# 5. CHECK EXTREME CORRELATIONS
# -----------------------------

print("\n--- Checking Top Correlations ---")

# corr = df.corr(numeric_only=True)["rainfall"].sort_values(ascending=False)
corr = numeric_df.corr()["rainfall"].sort_values(ascending=False)

print("\nTop correlations with rainfall:\n")
print(corr.head(10))


# -----------------------------
# 6. CHECK ZERO VARIANCE FEATURES
# -----------------------------

print("\n--- Checking Constant Features ---")

constant_cols = [c for c in df.columns if df[c].nunique() <= 1]

if constant_cols:
    print("⚠️ Constant columns found:")
    print(constant_cols)
else:
    print("No constant columns")


# -----------------------------
# 7. BASIC DATA SUMMARY
# -----------------------------

print("\n--- Rainfall Distribution ---")

print(df["rainfall"].describe())


print("\n====== VERIFICATION COMPLETE ======\n")