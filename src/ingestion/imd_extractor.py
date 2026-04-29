import xarray as xr
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import os
# Local imports
from src.config.settings import IMD_DATA_DIR, RAINFALL_DATASET, TARGET_LAT, TARGET_LON
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# This module extracts rainfall data from IMD NetCDF files for the target location and compiles it into a single CSV dataset.
def extract_point_rainfall(ds):
    """
    Extract rainfall from nearest grid point to target location.
    Handles different coordinate naming conventions.
    """
    if "LATITUDE" in ds.coords:
        rain = ds.sel(
            LATITUDE=TARGET_LAT,
            LONGITUDE=TARGET_LON,
            method="nearest"
        )
    elif "lat" in ds.coords:
        rain = ds.sel(
            lat=TARGET_LAT,
            lon=TARGET_LON,
            method="nearest"
        )
    else:
        raise ValueError("Unknown coordinate format")
    return rain

# Process a single NetCDF file and return a DataFrame with time and rainfall
def process_file(file_path):
    ds = xr.open_dataset(file_path)
    rain = extract_point_rainfall(ds)
    df = rain.to_dataframe().reset_index()
    ds.close()
    return df

# Main function to build the rainfall dataset
def build_rainfall_dataset():
    logger.info("Starting IMD rainfall extraction")
    files = sorted(IMD_DATA_DIR.glob("*.nc"))
    all_data = []
    for file in tqdm(files):
        logger.info(f"Processing {file.name}")
        df = process_file(file)
        all_data.append(df)
    final_df = pd.concat(all_data)
    logger.info("Saving rainfall dataset")

# Ensure output directory exists and save the final dataset
    os.makedirs(os.path.dirname(RAINFALL_DATASET), exist_ok=True)
    final_df.to_csv(RAINFALL_DATASET, index=False)
    logger.info("Rainfall dataset created successfully")

# Example usage:
if __name__ == "__main__":

    build_rainfall_dataset()