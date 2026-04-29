import pandas as pd
import os
# Local imports
from src.config.settings import PROCESSED_DATA_DIR

INPUT_FILE = PROCESSED_DATA_DIR / "rainfall_dataset.csv"
OUTPUT_FILE = PROCESSED_DATA_DIR / "imd_rainfall_clean.csv"

# This module cleans the raw IMD rainfall dataset by ensuring correct columns, formatting, and removing duplicates.
def clean_imd_dataset():
    print("Loading IMD rainfall dataset...")
    df = pd.read_csv(INPUT_FILE)
    # Use only correct IMD columns
    df = df[["TIME", "RAINFALL"]]
    df = df.rename(columns={
        "TIME": "date",
        "RAINFALL": "rainfall"
    })
    # Convert date to datetime and sort
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df = df.drop_duplicates(subset="date")
# Ensure output directory exists and save the final dataset
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print("Clean dataset saved:", OUTPUT_FILE)

# Example usage:
if __name__ == "__main__":
    clean_imd_dataset()