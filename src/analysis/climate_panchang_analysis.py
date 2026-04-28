import pandas as pd
import json
from pathlib import Path

# Define the data directory
DATA_DIR = Path("data")

# Load panchang dataset
def load_panchang():
    records = []
    with open(DATA_DIR / "raw/panchangam_dataset.jsonl") as f:
        for line in f:
            records.append(json.loads(line))
    return pd.DataFrame(records)

# Load weather dataset
def load_weather():
    return pd.read_csv(DATA_DIR / "processed/merged_imd-weather_dataset.csv")

# Merge the datasets based on the date column
def merge_datasets():
    # Load both datasets and merge on the date column
    panchang = load_panchang()
    weather = load_weather()
    panchang["date"] = pd.to_datetime(panchang["date"])
    weather["date"] = pd.to_datetime(weather["date"])
    df = pd.merge(weather, panchang, on="date")
    return df

## Analysis functions
# Rainfall by nakshatra analysis
def rainfall_by_nakshatra(df):
    # Assuming nakshatra is a categorical variable representing the nakshatra of the date
    result = (
        df.groupby("nakshatra")["rainfall"]
        .mean()
        .sort_values(ascending=False)
    )
    print("\nRainfall by Nakshatra")
    print(result)

# Rainfall by tithi analysis
def rainfall_by_tithi(df):
    # Assuming tithi is a categorical variable representing the tithi of the date
    result = (
        df.groupby("tithi")["rainfall"]
        .mean()
        .sort_values(ascending=False)
    )
    print("\nRainfall by Tithi")
    print(result)

# Correlation analysis between moon phase and rainfall
def moon_phase_correlation(df):
    # Assuming moon_phase is a categorical variable representing the moon phase of the date, we need to convert it to a numerical format for correlation analysis. We can use a simple mapping for the moon phases to numerical values.
    phase_map = {
        "New Moon":0,
        "Waxing Crescent":1,
        "First Quarter":2,
        "Waxing Gibbous":3,
        "Full Moon":4,
        "Waning Gibbous":5,
        "Last Quarter":6,
        "Waning Crescent":7
    }
    # Map the moon phases to numerical values
    df["moon_phase_num"] = df["moon_phase"].map(phase_map)

    corr = df["moon_phase_num"].corr(df["rainfall"])

    print("\nMoon Phase vs Rainfall correlation:")
    print(corr)

# Seasonal cycle analysis based on lunar months
def seasonal_cycle(df):
    # Assuming moon_phase is a categorical variable representing the moon phase of the date
    result = (
        df.groupby("moon_phase")["rainfall"]
        .mean()
        .sort_values(ascending=False)
    )

    print("\nRainfall by Moon Phase")
    print(result)

# Main analysis function
def run_analysis():
    df = merge_datasets()
    # Print available columns for reference
    print("\nAvailable Columns:")
    print(df.columns)

    rainfall_by_nakshatra(df)
    rainfall_by_tithi(df)
    moon_phase_correlation(df)
    seasonal_cycle(df)

# Example usage:
if __name__ == "__main__":
    run_analysis()