import pandas as pd

df = pd.read_csv("data/processed/master_dataset.csv")

# drop text columns
drop_cols = [
"tithi",
"nakshatra",
"yoga",
"karana",
"vara",
"moon_phase"
]

df = df.drop(columns=drop_cols)

# drop missing rows
df = df.dropna()

df.to_csv("data/processed/clean_dataset.csv", index=False)

print("Clean dataset saved")