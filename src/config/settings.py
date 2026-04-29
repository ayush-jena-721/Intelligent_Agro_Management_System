from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data directories
DATA_DIR = PROJECT_ROOT / "data" # Main data directory

RAW_DATA_DIR = DATA_DIR / "raw" # For original datasets as downloaded
INTERIM_DATA_DIR = DATA_DIR / "interim" # For intermediate files during processing
PROCESSED_DATA_DIR = DATA_DIR / "processed" # For final cleaned datasets ready for analysis/modeling

# Specific datasets
IMD_DATA_DIR = RAW_DATA_DIR / "imd_rainfall_nc" # Directory containing IMD rainfall data in NetCDF format
WEATHER_DATA_DIR = RAW_DATA_DIR / "weather_raw" # Directory containing raw weather data (e.g., from OpenWeatherMap API)
PANCHANGAM_DIR = RAW_DATA_DIR / "panchangam_raw" 


# Output datasets
RAINFALL_DATASET = PROCESSED_DATA_DIR / "rainfall_dataset.csv" # Processed rainfall data with relevant features extracted (e.g., daily rainfall, monthly aggregates)
WEATHER_DATASET = PROCESSED_DATA_DIR / "weather_dataset.csv" # Processed weather data with relevant features extracted (e.g., temperature, humidity, wind speed)
PANCHANGAM_DATASET = PROCESSED_DATA_DIR / "panchangam_dataset.csv" # Processed Panchangam data with relevant features extracted

FUSION_DATASET = PROCESSED_DATA_DIR / "fusion_dataset.csv" # Final dataset combining all features for modeling

# Model storage
MODEL_DIR = PROJECT_ROOT / "models" # Directory to save trained models and related artifacts (e.g., scalers, encoders)

# Target location (your area)
TARGET_LAT = 12.02 # Latitude for Auroville, Tamil Nadu, India
TARGET_LON = 79.56 # Longitude for Auroville, Tamil Nadu, India


# Example usage:
    # from src.config.settings import TARGET_LAT, TARGET_LON
    # from src.config.settings import IMD_DATA_DIR
