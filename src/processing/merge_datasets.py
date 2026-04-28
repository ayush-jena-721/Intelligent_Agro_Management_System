import pandas as pd
import json

# paths
climate_file = "data/processed/merged_imd-weather_dataset.csv"
panchang_file = "data/raw/panchangam_raw/panchangam_dataset.jsonl"

print("Loading climate dataset...")
climate = pd.read_csv(climate_file)

print("Loading panchang dataset...")
rows = []

# Load panchang dataset from JSONL file
with open(panchang_file) as f:
    for line in f:
        rows.append(json.loads(line))

panchang = pd.DataFrame(rows)

# convert dates
climate["date"] = pd.to_datetime(climate["date"])
panchang["date"] = pd.to_datetime(panchang["date"])

# Merge the datasets based on the date column
print("Merging datasets...")
merged = pd.merge(climate, panchang, on="date", how="inner")

# Save the merged dataset to a new CSV file
print("Saving merged dataset...")
merged.to_csv("data/processed/master_dataset.csv", index=False)

print("Merge complete")
print("Rows:", len(merged))