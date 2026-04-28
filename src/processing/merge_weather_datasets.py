import pandas as pd
import os
# Local imports
from src.config.settings import PROCESSED_DATA_DIR
# Input files
RAIN_FILE = PROCESSED_DATA_DIR / "imd_rainfall_clean.csv"
WEATHER_FILE = PROCESSED_DATA_DIR / "weather_dataset.csv"
OUTPUT_FILE = PROCESSED_DATA_DIR / "merged_imd-weather_dataset.csv"

# This module merges the cleaned IMD rainfall dataset with the weather dataset based on date, ensuring that only dates with both rainfall and weather data are included in the final dataset.
def merge_datasets():
    print("Loading datasets...")
    # Load the cleaned rainfall and weather datasets
    rain_df = pd.read_csv(RAIN_FILE)
    weather_df = pd.read_csv(WEATHER_FILE)
    # Convert date columns to datetime
    rain_df["date"] = pd.to_datetime(rain_df["date"])
    weather_df["date"] = pd.to_datetime(weather_df["date"])
    # Merge on date, keeping only rows where both rainfall and weather data are available
    print("Merging rainfall and weather datasets...")
    merged = pd.merge(
        rain_df,
        weather_df,
        on="date",
        how="inner"
    )
    merged = merged.sort_values("date")
    # Ensure output directory exists and save the final dataset
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    merged.to_csv(OUTPUT_FILE, index=False)
    print("Final weather dataset saved:")
    print(OUTPUT_FILE)
    print("Dataset shape:", merged.shape)

# Example usage:
if __name__ == "__main__":
    merge_datasets()