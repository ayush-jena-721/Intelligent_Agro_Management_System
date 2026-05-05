# 📋 **MEGHDRISTI WEATHER INTELLIGENCE - COMPLETE PROJECT SPECIFICATION**

## **🎯 PROJECT OVERVIEW**
**MeghDristi** is a comprehensive weather prediction and agricultural intelligence system that combines:
- **Indian Meteorological Department (IMD)** rainfall data (1924-present)
- **Open-Meteo API** weather data (1940-present)
- **Vedic Panchangam** (lunar calendar) astronomical calculations
- **Machine Learning** (XGBoost/LightGBM) for rainfall prediction
- **Streamlit** web dashboard & **FastAPI** REST backend

**Target Location:** Villupuram, Tamil Nadu, India (12.02°N, 79.56°E)

---

## **📊 DATA PIPELINE FLOW**

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA INGESTION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  IMD Rainfall (NetCDF)    +    OpenMeteo Weather API             │
│  (1924-present)           +    (1940-present)                    │
└──────────────┬──────────────────────────────────────┬────────────┘
               │                                      │
┌──────────────▼──────────────────────────────────────▼────────────┐
│                    DATA CLEANING LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  - Remove duplicates, handle missing values                      │
│  - Standardize column names and formats                         │
│  - Convert hourly → daily aggregates                            │
└──────────────┬──────────────────────────────────────┬────────────┘
               │                                      │
               └──────────────┬─────────────────────┬─┘
                              │  MERGE              │
         ┌────────────────────▼──────────────────────▼────┐
         │    Panchangam Data (Lunar Calendar)            │
         │  (Generated for 1940-2025 daily at sunrise)   │
         └────────────────────┬──────────────────────────┘
                              │
┌─────────────────────────────▼──────────────────────────────────┐
│              EXPLORATORY DATA ANALYSIS (EDA)                    │
├─────────────────────────────────────────────────────────────────┤
│  - Correlation Analysis      - Rainfall Cycle Detection (FFT)  │
│  - Climate-Panchangam Analysis                                 │
└─────────────────────────────┬──────────────────────────────────┘
                              │
┌─────────────────────────────▼──────────────────────────────────┐
│            FEATURE ENGINEERING & ENCODING                       │
├─────────────────────────────────────────────────────────────────┤
│  Time Features: Year, Month, Day, Day-of-Year, Cyclical        │
│  Lag Features: 1, 3, 7, 14-day rainfall lags                   │
│  Rolling Stats: 3, 7, 14, 30-day windows (mean/std)            │
│  Encoding: Circular (sin/cos), Categorical (one-hot)           │
└─────────────────────────────┬──────────────────────────────────┘
                              │
┌─────────────────────────────▼──────────────────────────────────┐
│         TRAIN/VALIDATION/TEST SPLIT (Time-series)              │
├─────────────────────────────────────────────────────────────────┤
│  80% Training  →  20% Validation/Test                          │
└─────────────────────────────┬──────────────────────────────────┘
                              │
┌─────────────────────────────▼──────────────────────────────────┐
│              MODEL TRAINING & BACKTESTING                       │
├─────────────────────────────────────────────────────────────────┤
│  XGBoost / LightGBM Regression                                 │
│  Metrics: MAE, RMSE, R² Score                                  │
└─────────────────────────────┬──────────────────────────────────┘
                              │
┌─────────────────────────────▼──────────────────────────────────┐
│         PREDICTION & AGRICULTURE ADVICE                         │
├─────────────────────────────────────────────────────────────────┤
│  - Daily rainfall forecast (mm)                                │
│  - Rain probability (%)                                        │
│  - Agriculture recommendations (seed, irrigation, spray)       │
└─────────────────────────────────────────────────────────────────┘
```

---

## **📁 PROJECT FOLDER STRUCTURE**

```
Final_MD/
├── 📄 requirements.txt             [Python dependencies]
├── 📄 Pipeline-Flow.txt            [Data pipeline documentation]
├── 📄 Working-Command.txt          [Script execution order]
├── 📄 de440s.bsp                   [Ephemeris data for astronomy]
│
├── 📂 data/                        [Complete dataset directory]
│   ├── raw/                        [Raw ingested data]
│   │   ├── imd_rainfall_nc/        [IMD NetCDF files 1924-2025]
│   │   └── panchangam_raw/         [Panchangam JSONL data]
│   ├── interim/                    [Intermediate processing]
│   └── processed/                  [Final clean datasets]
│       ├── clean_dataset.csv
│       ├── feature_dataset.csv
│       ├── master_dataset.csv
│       ├── merged_imd-weather_dataset.csv
│       ├── rainfall_dataset.csv
│       ├── weather_dataset.csv
│       └── weather_features.csv
│
├── 📂 models/                      [Trained ML models & results]
│   ├── xgboost_rainfall_model.json
│   ├── feature_importance.csv
│   └── backtest_results.csv
│
├── 📂 src/                         [Main source code]
│   ├── 📂 ingestion/               [Data collection from sources]
│   │   ├── imd_extractor.py        → Extract rainfall from NetCDF
│   │   └── openmeteo_fetcher.py    → Fetch weather from API
│   │
│   ├── 📂 processing/              [Data cleaning & merging]
│   │   ├── clean_dataset.py        → Remove NULLs & text columns
│   │   ├── clean_imd_rainfall.py   → Clean IMD rainfall data
│   │   ├── merge_weather_datasets.py → Merge IMD + weather data
│   │   └── merge_datasets.py       → Merge weather + panchangam
│   │
│   ├── 📂 panchangam/              [Vedic astronomy module]
│   │   ├── constants.py            → Tithi, Nakshatra, etc. names
│   │   ├── panchangam_calculator.py→ Core astronomical calculations
│   │   ├── panchangam_generator.py → Generate dataset 1940-2025
│   │   └── utils.py                → Decode panchangam indices
│   │
│   ├── 📂 analysis/                [Exploratory Data Analysis]
│   │   ├── climate_panchang_analysis.py → Analyze climate-lunar relationships
│   │   ├── correlation_analysis.py     → Feature-target correlations
│   │   └── rainfall_cycle_detector.py  → Fourier FFT analysis
│   │
│   ├── 📂 features/                [Feature Engineering]
│   │   └── feature_engineering.py  → Create time-series features
│   │
│   ├── 📂 models/                  [ML Training & Evaluation]
│   │   ├── train_xgboost.py        → Train XGBoost model
│   │   ├── backtest_models.py      → Evaluate on historical data
│   │   └── verify_pipeline.py      → Check for data leakage
│   │
│   ├── 📂 predict/                 [Prediction Engine]
│   │   ├── predict_engine.py       → Main forecasting & advice
│   │   └── predict_rainfall.py     → Multi-day forecast
│   │
│   ├── 📂 config/                  [Project Configuration]
│   │   └── settings.py             → File paths & constants
│   │
│   ├── 📂 api/                     [REST API Backend]
│   │   └── app.py                  → FastAPI endpoints
│   │
│   ├── 📂 webapp/                  [Streamlit Web Frontend]
│   │   ├── app.py                  → Main dashboard app
│   │   ├── dashboard.py            → Weather metrics display
│   │   ├── forecast.py             → Multi-day forecast UI
│   │   ├── analytics.py            → Data analysis visualizations
│   │   └── ai_panel.py             → AI agriculture advisor
│   │
│   └── 📂 utils/                   [Utilities]
│       └── logger.py               → Logging setup
│
└── 📂 myenv/                       [Python virtual environment]
```

---

## **⚙️ DEPENDENCIES (from requirements.txt)**

| Category | Libraries |
|----------|-----------|
| **Data Processing** | numpy, pandas, xarray, netCDF4 |
| **Visualization** | matplotlib, seaborn |
| **Machine Learning** | scikit-learn, xgboost, lightgbm, joblib, scipy |
| **Astronomy** | astral, skyfield, jplephem |
| **API & Web** | requests, streamlit, uvicorn (implicit from FastAPI) |
| **Utilities** | tqdm, python-dateutil, pytz, loguru |

---

## **🔧 ALL SCRIPTS - DETAILED SPECIFICATION**

### **1️⃣ INGESTION LAYER** - Collect External Data

#### **imd_extractor.py**
```
PURPOSE:    Extract rainfall from Indian Meteorological Dept (IMD) NetCDF files
INPUT:      NetCDF files in data/raw/imd_rainfall_nc/ (1924.nc - 2025.nc)
OUTPUT:     data/processed/rainfall_dataset.csv
FUNCTIONS:
  ├─ extract_point_rainfall(ds)  - Extract nearest grid point to target
  ├─ process_file(file_path)     - Process single year NetCDF
  └─ build_rainfall_dataset()    - Compile all years into one CSV
METHOD:     Uses xarray to read NetCDF, finds nearest grid to (12.02°N, 79.56°E)
```

#### **openmeteo_fetcher.py**
```
PURPOSE:    Fetch weather data from Open-Meteo Historical Weather API
INPUT:      API requests for years 1940-2026
OUTPUT:     data/processed/weather_dataset.csv
FUNCTIONS:
  ├─ fetch_year(lat, lon, start, end)     - Fetch hourly data for year range
  ├─ convert_hourly_to_daily(df)          - Aggregate to daily (mean temp, sum rain)
  └─ build_weather_dataset()              - Compile all years
VARIABLES:  temperature_2m, relativehumidity_2m, dewpoint_2m, 
           apparent_temperature, surface_pressure, precipitation
```

---

### **2️⃣ PROCESSING LAYER** - Clean & Merge Data

#### **clean_imd_rainfall.py**
```
PURPOSE:    Clean raw IMD rainfall dataset
INPUT:      data/processed/rainfall_dataset.csv (raw from extractor)
OUTPUT:     data/processed/imd_rainfall_clean.csv
OPERATIONS: ✓ Dropna (remove missing values)
            ✓ Remove duplicates
            ✓ Standardize column names
            ✓ Date validation
```

#### **merge_weather_datasets.py**
```
PURPOSE:    Merge IMD rainfall with weather data
INPUT:      imd_rainfall_clean.csv + weather_dataset.csv
OUTPUT:     merged_imd-weather_dataset.csv
METHOD:     Inner join on date (only matching dates kept)
RESULT:     Combined rainfall & weather for same dates
```

#### **clean_dataset.py**
```
PURPOSE:    Remove text columns & missing values from master dataset
INPUT:      master_dataset.csv (with all panchangam text)
OUTPUT:     clean_dataset.csv (features only)
REMOVES:    tithi, nakshatra, yoga, karana, vara (text columns)
            All NaN rows
```

#### **merge_datasets.py**
```
PURPOSE:    Merge climate data with Panchangam dataset
INPUT:      merged_imd-weather_dataset.csv + panchangam_dataset.jsonl
OUTPUT:     master_dataset.csv (complete fusion)
METHOD:     Join on date, load JSONL panchangam data
RESULT:     Every row has: weather + rainfall + panchangam
```

---

### **3️⃣ ANALYSIS LAYER** - Explore & Understand Data

#### **rainfall_cycle_detector.py**
```
PURPOSE:    Detect cyclical patterns in rainfall using Fourier Transform
INPUT:      merged_imd-weather_dataset.csv
OUTPUT:     FFT analysis plots showing dominant frequencies
FUNCTIONS:
  ├─ load_data()           - Load & prepare dataset
  ├─ detect_cycles(df)     - Apply FFT to find periodicities
  ├─ plot_cycles(xf, power) - Visualize frequency spectrum
  └─ run()                 - Main execution
METHOD:     Uses scipy.fft to find recurring rainfall patterns
```

#### **correlation_analysis.py**
```
PURPOSE:    Analyze feature-target correlations
INPUT:      clean_dataset.csv
OUTPUT:     Correlation matrix + heatmap visualization
OPERATIONS: ✓ Compute Pearson correlation for all features with rainfall
            ✓ Generate heatmap showing relationships
```

#### **climate_panchang_analysis.py**
```
PURPOSE:    Analyze relationships between climate & lunar calendar
INPUT:      panchangam_dataset.jsonl + weather_dataset.csv
OUTPUT:     Rainfall statistics by lunar day/mansion
FUNCTIONS:
  ├─ rainfall_by_nakshatra(df) - Mean rainfall for each lunar mansion
  ├─ rainfall_by_tithi(df)     - Mean rainfall for each lunar day
  └─ merge_datasets()          - Combine datasets
INSIGHT:    Does rainfall correlate with lunar phases?
```

---

### **4️⃣ FEATURES LAYER** - Engineer Features for ML

#### **feature_engineering.py**
```
PURPOSE:    Create time-series features for ML models
STATUS:     ⚠️ Currently COMMENTED (partial implementation)
PLANNED FEATURES:
  ├─ TIME FEATURES
  │   ├─ year, month, day, day_of_year
  │   ├─ Cyclical encoding (sin/cos of month & day)
  │   └─ monsoon_flag (indicator for monsoon season)
  │
  ├─ LAG FEATURES (rainfall history)
  │   ├─ rainfall_lag_1, _3, _7, _14 days
  │   └─ Captures recent rainfall patterns
  │
  └─ ROLLING STATISTICS (3, 7, 14, 30-day windows)
      ├─ mean, std, min, max for each window
      └─ Captures trends & volatility
```

---

### **5️⃣ MODELS LAYER** - Train & Validate

#### **train_xgboost.py**
```
PURPOSE:    Train XGBoost regression for rainfall prediction
STATUS:     ⚠️ Currently COMMENTED (reference implementation)
INPUT:      weather_features.csv (with engineered features)
OUTPUT:     xgboost_rainfall_model.pkl (saved model)
TRAINING:
  ├─ Train/Val/Test Split: 80% train → 75% val / 25% test
  ├─ Time-series aware (no future data leakage)
  ├─ Target: rainfall (mm)
  └─ XGBoost 3.x compatible API
PARAMETERS: (tuned via hyperparameter search)
  ├─ n_estimators: 100-500
  ├─ max_depth: 5-10
  ├─ learning_rate: 0.01-0.1
  └─ regularization (L1/L2)
```

#### **backtest_models.py**
```
PURPOSE:    Backtest trained models on historical data
INPUT:      weather_features.csv + trained model (PKL)
OUTPUT:     backtest_results.csv + performance metrics
METRICS:    ✓ MAE (Mean Absolute Error)
            ✓ RMSE (Root Mean Squared Error)
            ✓ R² Score (coefficient of determination)
FUNCTIONS:
  └─ evaluate(y_true, y_pred, name) - Compute all metrics
```

#### **verify_pipeline.py**
```
PURPOSE:    Validate pipeline integrity (no data leakage)
INPUT:      weather_features.csv
CHECKS:
  ├─ ⚠️ Target Leakage: flags features with corr >= 0.95 to target
  ├─ ⚠️ Future Data: finds features with "lead", "future", "t+"
  ├─ ✓ Null Values: counts missing data
  └─ ✓ Data Types: validates feature types
OUTPUT:     Pass/Fail status with warnings
```

---

### **6️⃣ PANCHANGAM LAYER** - Vedic Astronomy

#### **constants.py**
```
PURPOSE:    Define all Panchangam factor names
CONSTANTS:
  ├─ TITHI_NAMES (30): Pratipada, Dvitiya, ..., Amavasya
  │                    (lunar days - 30 in a lunar month)
  ├─ NAK_NAMES (27):   Ashwini, Bharani, Krittika, ..., Revati
  │                    (lunar mansions - 27 constellations)
  ├─ YOGA_NAMES (27):  27 yoga (time units in astrology)
  ├─ KARANA_NAMES (11): 11 karanas (half-tithi divisions)
  └─ VARA_NAMES (7):   Ravivara (Sunday), Somavara (Monday), ...
                        (Sanskrit weekday names)
```

#### **panchangam_calculator.py**
```
PURPOSE:    Core astronomical calculations using Skyfield ephemeris
DATA:       Uses de440s.bsp (NASA ephemeris file for accurate positions)
FUNCTIONS:
  ├─ get_longitudes(time)         → Sun & Moon ecliptic longitudes
  ├─ calculate_tithi(sun_lon, moon_lon)
  │   └─ Divides 360° × 2 into 30 lunar days, finds current day
  ├─ calculate_nakshatra(moon_lon)
  │   └─ Divides moon's 360° path into 27 lunar mansions
  ├─ calculate_yoga(sun_lon, moon_lon)
  │   └─ Sum of longitudes divided by 27
  ├─ calculate_karana(sun_lon, moon_lon)
  │   └─ Half-tithi (60 divisions of lunar month)
  ├─ calculate_vara(time)
  │   └─ Day of week (0=Monday, 6=Sunday)
  ├─ calculate_moon_phase(time)
  │   └─ Phase name + angle (0°=New Moon, 180°=Full Moon)
  └─ calculate_moon_distance(time)
      └─ Moon's distance from Earth in km
AYANAMSA:   Lahiri ayanamsa (+23.15°) - converts tropical to sidereal
```

#### **panchangam_generator.py**
```
PURPOSE:    Generate complete Panchangam dataset for 1940-2025
INPUT:      None (generates from astronomical calculations)
OUTPUT:     data/raw/panchangam_dataset.jsonl (one JSON per line)
LOCATION:   Villupuram, Tamil Nadu (11.94°N, 79.49°E)
TIME:       Calculated at sunrise each day (Asia/Kolkata timezone)
SCOPE:      1940-01-01 to 2025-12-31 (~86,000 days)
RECORD FORMAT per line:
{
  "date": "1940-01-01",
  "tithi_index": 2,
  "tithi": "Tritiya",
  "nakshatra_index": 3,
  "nakshatra": "Krittika",
  "yoga_index": 5,
  "yoga": "yoga_name",
  "karana_index": 1,
  "karana": "Balava",
  "vara_index": 3,
  "vara": "Budhavara",
  "moon_phase": "Waning Crescent",
  "moon_phase_angle": 15.2,
  "moon_distance_km": 405600
}
PROCESS:    For each day, calculate astronomical positions, find lunar day/mansion,
            apply Lahiri ayanamsa correction for accuracy
```

#### **utils.py**
```
PURPOSE:    Utility functions for Panchangam data handling
FUNCTIONS:
  └─ decode_panchang(row) → Convert indices to readable names
     INPUT:  {"tithi_index": 2, "nakshatra_index": 3, ...}
     OUTPUT: {"tithi": "Tritiya", "nakshatra": "Krittika", ...}
```

---

### **7️⃣ PREDICT LAYER** - Generate Forecasts

#### **predict_engine.py**
```
PURPOSE:    Main prediction engine for rainfall & agriculture advice
INPUT:      Trained model + Latest weather + Panchangam data
FUNCTIONS:
  ├─ forecast(days=5)
  │   ├─ Generate multi-day rainfall forecast
  │   ├─ Outputs: date, rainfall_mm, probability, condition
  │   └─ Returns list of forecast dicts
  │
  ├─ get_current_weather()
  │   └─ Extract latest weather & panchangam values
  │
  ├─ rain_condition(rain)
  │   └─ Categorize rainfall into 5 levels
  │       • No Rain (0-2 mm)
  │       • Light (2-10 mm)
  │       • Moderate (10-25 mm)
  │       • Heavy (25-50 mm)
  │       • Very Heavy (>50 mm)
  │
  ├─ rain_probability(rain)
  │   └─ Convert rainfall amount to percentage (10%-95%)
  │
  └─ agriculture_advice(rain, humidity)
      └─ Recommend: seed planting, irrigation, pesticide spray
         based on weather conditions
MODEL:     LightGBM (models/lightgbm_rainfall_model.pkl)
```

#### **predict_rainfall.py**
```
PURPOSE:    Multi-day rainfall forecast generation
INPUT:      weather_features.csv + trained model
OUTPUT:     5-day forecast with emoji-based conditions
FUNCTIONS:
  ├─ rain_condition(value) → emoji text representation
  └─ Format & print forecast
```

---

### **8️⃣ CONFIG LAYER** - Centralized Settings

#### **settings.py**
```
PURPOSE:    Centralized configuration for entire project
DEFINES:
  ├─ Paths:
  │   ├─ PROJECT_ROOT → project directory root
  │   ├─ DATA_DIRS → raw, interim, processed
  │   ├─ DATASET_PATHS → all CSV file locations
  │   └─ MODEL_DIR → model storage location
  │
  └─ Constants:
      ├─ TARGET_LAT = 12.02° (Cuddalore)
      ├─ TARGET_LON = 79.56° (Cuddalore)
      └─ Other project-wide constants
USAGE:     Import in other modules: from src.config.settings import PROCESSED_DATA_DIR
```

---

### **9️⃣ API LAYER** - REST Backend

#### **app.py**
```
PURPOSE:    FastAPI REST backend for rainfall predictions
FRAMEWORK:  FastAPI (async Python web framework)
ENDPOINTS:
  ├─ GET /
  │   └─ Health check → {"message":"MeghDristi System Running"}
  │
  └─ GET /forecast
      ├─ Get 5-day forecast
      ├─ Get current weather & panchangam
      └─ Response: {"forecast": [...], "weather": {...}}
RUN:       uvicorn src.api.app:app --reload
PORT:      Default 8000
```

---

### **🔟 WEBAPP LAYER** - Streamlit Frontend

#### **app.py** (Main Entry)
```
PURPOSE:    Main Streamlit app orchestrator
STATUS:     ⚠️ Currently COMMENTED
STRUCTURE:  Multi-page app with navigation
CONFIG:     Title: "MeghDristi Weather Intelligence"
            Icon: "🌧"
            Layout: Wide
PAGES:      (imports from other modules)
```

#### **dashboard.py**
```
PURPOSE:    Display weather metrics dashboard
DISPLAY:    ┌─────────────────────────────────────┐
            │ Rainfall (mm)    │ Rain Prob (%)   │
            │ Temp (°C)        │ Humidity (%)    │
            └─────────────────────────────────────┘
            Plus Panchangam conditions (tithi, nakshatra, etc.)
FUNCTIONS:
  └─ show_dashboard() → Render Streamlit dashboard
```

#### **forecast.py**
```
PURPOSE:    Display multi-day forecast UI
DISPLAY:    Day-by-day forecast with:
            ├─ Date
            ├─ Rainfall prediction
            ├─ Rain probability
            ├─ Weather condition emoji
            └─ Agriculture advice
```

#### **analytics.py**
```
PURPOSE:    Display data analysis visualizations
CHARTS:     ├─ Feature importances (bar plot)
            ├─ Correlation heatmap
            ├─ Historical rainfall trends
            ├─ Seasonal patterns
            └─ Model performance metrics
```

#### **ai_panel.py**
```
PURPOSE:    AI-powered agriculture advisor
FEATURES:   ├─ Crop recommendation engine
            ├─ Planting schedule suggestions
            ├─ Irrigation timing
            ├─ Pesticide spray recommendations
            └─ Yield predictions based on weather
```

---

### **1️⃣1️⃣ UTILS LAYER**

#### **logger.py**
```
PURPOSE:    Standardized logging across project
FUNCTION:
  └─ setup_logger(name: str)
     ├─ Creates logger with given name
     ├─ Sets INFO level
     ├─ Formats messages with [timestamp] [level] [message]
     └─ Outputs to console
USAGE:      from src.utils.logger import setup_logger
            logger = setup_logger(__name__)
```

---

## **📋 DATA FILES REFERENCE**

| File | Type | Size | Records | Purpose |
|------|------|------|---------|---------|
| `imd_rainfall_nc/1924.nc` ... `.nc` | NetCDF | ~5MB each | Grid data | Raw IMD rainfall |
| `rainfall_dataset.csv` | CSV | ~50MB | ~30,000 | Raw IMD extracted |
| `imd_rainfall_clean.csv` | CSV | ~45MB | ~30,000 | Cleaned IMD data |
| `weather_dataset.csv` | CSV | ~80MB | ~30,000 | API weather data |
| `merged_imd-weather_dataset.csv` | CSV | ~100MB | ~30,000 | Climate fusion |
| `panchangam_dataset.jsonl` | JSONL | ~30MB | ~31,500 | Lunar calendar |
| `master_dataset.csv` | CSV | ~150MB | ~30,000 | Complete dataset |
| `clean_dataset.csv` | CSV | ~80MB | ~28,000 | Features + target |
| `weather_features.csv` | CSV | ~100MB | ~28,000 | Engineered features |
| `xgboost_rainfall_model.json` | JSON | ~5MB | - | Trained model |

---

## **🚀 EXECUTION WORKFLOW**

```bash
# 1. Setup environment
pip install -r requirements.txt

# 2. Ingest data
python -m src.ingestion.imd_extractor          # Extract NetCDF rainfall
python -m src.ingestion.openmeteo_fetcher      # Fetch weather API

# 3. Generate Panchangam
python -m src.panchangam.panchangam_generator  # Create lunar calendar

# 4. Clean data
python -m src.processing.clean_imd_rainfall
python -m src.processing.merge_weather_datasets

# 5. Analysis
python -m src.analysis.climate_panchang_analysis
python -m src.analysis.rainfall_cycle_detector
python -m src.processing.merge_datasets
python -m src.processing.clean_dataset
python -m src.analysis.correlation_analysis

# 6. Features & Training
python -m src.features.feature_engineering
python -m src.models.train_xgboost
python -m src.models.verify_pipeline
python -m src.models.backtest_models

# 7. Prediction & Serving
python -m src.predict.predict_rainfall
uvicorn src.api.app:app --reload              # Start API on :8000
streamlit run src/webapp/app.py               # Start dashboard on :8501
```

---

## **📊 MODEL PERFORMANCE**

**Current Model:** XGBoost/LightGBM Regression  
**Target Variable:** Daily Rainfall (mm)  
**Features:** 30-50 engineered features (time, lags, rolling stats, panchangam)  
**Output Files:**
- `feature_importance.csv` - Which features matter most
- `backtest_results.csv` - Validation metrics (MAE, RMSE, R²)

---

**Last Updated:** March 18, 2026
