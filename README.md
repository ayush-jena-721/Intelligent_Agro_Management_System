# 🌧️ MeghDristi — Intelligent Rainfall Prediction & IoT-Based Smart Irrigation System

> **Final Year Project — Phase 1 + Phase 2**
> **AI-Based Rainfall Intelligence + Real-World IoT Irrigation Demonstration**

MeghDristi is an intelligent agriculture proof-of-concept that combines **machine learning, meteorological data, astronomical/Panchangam-derived features, environmental sensing, IoT, web technology, and automated irrigation**.

The project evolved through two major phases:

* **Phase 1:** AI-based rainfall intelligence using historical meteorological and astronomical data.
* **Phase 2:** ESP32-based IoT irrigation using real ground/soil conditions and a working web-host interface.

The overall pipeline is:

```text
Historical Data
      ↓
Weather Intelligence
      ↓
Machine Learning
      ↓
Environmental / Soil Data
      ↓
ESP32 IoT Controller
      ↓
Web Interface
      ↓
Irrigation Control
      ↓
Real-World Agricultural Application
```

## Table of Contents

1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [Motivation](#-motivation)
4. [Proposed Solution](#-proposed-solution)
5. [Project Evolution](#-project-evolution)
6. [Phase 1 — Rainfall Intelligence](#-phase-1--rainfall-intelligence)
7. [Phase 2 — IoT Smart Irrigation](#-phase-2--iot-smart-irrigation)
8. [System Architecture](#-system-architecture)
9. [Hardware Components](#-hardware-components)
10. [Software Components](#-software-components)
11. [Data Flow](#-data-flow)
12. [ESP32 and IoT Layer](#-esp32-and-iot-layer)
13. [Web Interface](#-web-interface)
14. [Irrigation Control](#-irrigation-control)
15. [Installation](#-installation)
16. [Usage](#-usage)
17. [Demonstration](#-demonstration)
18. [Results](#-results)
19. [Testing](#-testing)
20. [Project Structure](#-project-structure)
21. [Technology Stack](#-technology-stack)
22. [Implementation Status](#-implementation-status)
23. [Security Considerations](#-security-considerations)
24. [Limitations](#-limitations)
25. [Future Scope](#-future-scope)
26. [Success Criteria](#-success-criteria)
27. [Project Team](#-project-team)
28. [Documentation](#-documentation)
29. [License](#-license)
30. [Conclusion](#-conclusion)

---

## 🌱 Project Overview

Agriculture depends heavily on environmental conditions such as **rainfall, soil moisture, temperature, humidity, and water availability**.

MeghDristi connects two traditionally separate areas:

1. **Predictive intelligence** — understanding weather and rainfall patterns.
2. **Physical agricultural control** — observing ground conditions and controlling irrigation.

### Phase 1

Phase 1 developed a hybrid rainfall-prediction framework using:

* Historical meteorological data
* Astronomical information
* Panchangam-derived data
* Feature engineering
* Machine learning
* XGBoost

### Phase 2

Phase 2 extended the project into a physical IoT proof-of-concept using:

* Soil/ground-condition sensing
* ESP32
* Network communication
* Web-hosted interaction
* Irrigation control

The project therefore progressed from **data and modelling** toward **physical agricultural interaction**.

---

## ❗ Problem Statement

Farmers must make irrigation decisions despite changing environmental conditions.

Common challenges include:

* Uncertain rainfall
* Over-irrigation
* Under-irrigation
* Water wastage
* Lack of continuous soil-condition monitoring
* Manual irrigation control
* Disconnect between weather information and ground conditions

Rainfall prediction alone does not determine the immediate irrigation requirement of a particular area. Similarly, a soil sensor alone cannot provide broader rainfall intelligence.

MeghDristi therefore explores:

```text
Weather Prediction
       +
Ground Condition Monitoring
       +
IoT Control
       =
Intelligent Irrigation
```

---

## 🎯 Motivation

The project was motivated by the need to move beyond a purely software-based prediction model and demonstrate how environmental intelligence can be connected to a physical agricultural system.

The original Phase 1 work identified several future agricultural applications, including:

* Soil-moisture sensing
* Temperature/humidity sensing
* Automated irrigation
* Crop recommendation
* Plant-disease detection
* Real-time farmer dashboards

Phase 2 represents the transition:

> **From predicting environmental conditions to interacting with real environmental conditions.**

---

## 💡 Proposed Solution

MeghDristi uses a layered architecture.

### Layer 1 — Historical Intelligence

Historical meteorological and astronomical data are processed to identify rainfall patterns.

### Layer 2 — Machine Learning

Machine-learning models investigate rainfall behaviour and prediction.

### Layer 3 — Ground Reality

Environmental and soil conditions are collected from the physical setup.

### Layer 4 — IoT

An **ESP32** provides the embedded hardware and control layer.

### Layer 5 — Web Interface

A working web-host interface provides a software-facing interface for observing and interacting with the IoT system.

### Layer 6 — Irrigation

The irrigation mechanism provides the physical actuation layer.

---

# 🚀 Project Evolution

## Phase 1 — AI Rainfall Intelligence

```text
Meteorological Data
        +
Astronomical Data
        ↓
Data Processing
        ↓
Feature Engineering
        ↓
Machine Learning
        ↓
Rainfall Prediction
```

The Phase 1 objective was to investigate rainfall prediction by integrating meteorological information with astronomical features and validating the approach through machine learning.

## Phase 2 — IoT Smart Irrigation

```text
Physical Soil / Environmental Conditions
                 ↓
               Sensors
                 ↓
                ESP32
                 ↓
         Web Communication
                 ↓
          Control Interface
                 ↓
         Irrigation Mechanism
```

Phase 2 successfully demonstrated:

* Physical IoT hardware
* ESP32 operation
* Soil/ground-condition data collection
* Web-hosted interface
* Software-to-hardware communication
* Irrigation control
* End-to-end physical operation

---

# 🌦️ Phase 1 — Rainfall Intelligence

Phase 1 was titled:

> **AI-Based Rainfall Prediction using Astronomical & Meteorological Data**

### Main technologies

* Python
* Machine Learning
* XGBoost
* Skyfield
* Open-Meteo API
* Panchangam-derived data

### Meteorological Data

The project documentation describes meteorological data from:

* IMD
* Open-Meteo

Parameters include:

* Rainfall
* Temperature
* Humidity

The repository architecture also supports spatial rainfall processing using latitude and longitude.

### Astronomical Data

Astronomical information was generated using **Skyfield**.

Documented features include:

* Lunar phase
* Moon age
* Planetary positions
* Astronomical timestamps

These features were converted into numerical features for machine-learning experiments.

### Panchangam Dataset

The Phase 1 workflow generated approximately **100 years of Panchangam data**, described as covering **1925–2025**, using astronomical calculations for Irumbai, Tamil Nadu, with IST timezone.

The resulting daily information was stored in JSONL format and used as an astronomical input to the rainfall-modelling workflow.

### Feature Engineering

The documented pipeline includes:

```text
Rainfall lag features
Rolling rainfall statistics
Month
Day of year
Week of year
Monsoon indicator
Astronomical features
Panchangam features
```

The documented binary target uses:

```text
Rainfall threshold = 2.5 mm
Target shift       = 2 days
```

This creates a **T+2 rainfall-occurrence prediction task**.

---

# 🌱 Phase 2 — IoT Smart Irrigation

Phase 2 extended MeghDristi from a data/ML prototype to a physical proof-of-concept.

The central objective was:

> **Collect ground-level soil/environmental information and demonstrate IoT-controlled irrigation using an ESP32 and a web interface.**

Unlike Phase 1, Phase 2 introduced **real-world physical data and hardware interaction**.

## Ground Reality Layer

The prototype collects information related to:

* Soil condition
* Ground condition
* Environmental state relevant to irrigation

This creates an important distinction:

```text
Phase 1:
"What does historical/weather data tell us?"

Phase 2:
"What is actually happening at the ground?"
```

The architecture therefore moves toward:

```text
Prediction + Measurement
```

rather than prediction alone.

---

# 🏗️ System Architecture

The complete system combines the two project phases:

```text
                     ┌────────────────────────┐
                     │      PHASE 1 DATA      │
                     ├────────────────────────┤
                     │ Historical Weather     │
                     │ Rainfall               │
                     │ Temperature            │
                     │ Humidity               │
                     │ Panchangam             │
                     │ Astronomical Features  │
                     └───────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │    MACHINE LEARNING    │
                     ├────────────────────────┤
                     │ XGBoost                │
                     │ Feature Engineering    │
                     │ Rainfall Prediction    │
                     └───────────┬────────────┘
                                 │
                                 ▼
              ┌─────────────────────────────────┐
              │       AGRICULTURAL LAYER        │
              ├─────────────────────────────────┤
              │                                 │
              │      Ground / Soil Data         │
              │              │                  │
              │              ▼                  │
              │          Sensors                │
              │              │                  │
              │              ▼                  │
              │           ESP32                 │
              │              │                  │
              │       ┌──────┴──────┐           │
              │       │             │           │
              │       ▼             ▼           │
              │    Web Host     Irrigation      │
              │                   Control       │
              │                     │            │
              │                     ▼            │
              │                 Water Supply    │
              └─────────────────────────────────┘
```

---

# 🔌 IoT Architecture

```text
       ┌────────────────────────────┐
       │       PHYSICAL SETUP       │
       │                            │
       │   Soil / Ground Condition  │
       └─────────────┬──────────────┘
                     │
                     ▼
               ┌──────────────┐
               │    SENSOR    │
               └──────┬───────┘
                      │
                      ▼
               ┌──────────────┐
               │    ESP32     │
               │              │
               │ Data Reading │
               │ Processing   │
               │ Networking   │
               │ Control      │
               └──────┬───────┘
                      │
              ┌───────┴────────┐
              │                │
              ▼                ▼
        ┌───────────┐    ┌─────────────┐
        │ Web Host  │    │ Irrigation  │
        │ Interface │    │ Mechanism   │
        └───────────┘    └──────┬──────┘
                                │
                                ▼
                              WATER
```

---

# 🔧 Hardware Components

| Component                      | Role                                    |
| ------------------------------ | --------------------------------------- |
| **ESP32**                      | Main IoT controller                     |
| **Soil/environment sensor(s)** | Collect ground-condition information    |
| **Irrigation actuator**        | Controls water delivery                 |
| **Water source**               | Supplies irrigation water               |
| **Power supply**               | Powers IoT and actuator components      |
| **Physical soil/plant setup**  | Represents the agricultural environment |

> **Note:** The exact sensor and actuator part numbers are not specified in the supplied documentation and should be added according to the final hardware BOM.

---

# 💻 Software Components

## Phase 1

The documented software stack includes:

* Python
* Pandas
* NumPy
* Xarray
* Scikit-learn
* XGBoost
* Skyfield
* PyJHora
* PyArrow
* Parquet

The broader project documentation also references visualization, web/API, validation, cloud, and AI libraries.

## Phase 2

The IoT layer adds:

* ESP32 firmware
* Sensor communication
* Network communication
* Web-host interface
* IoT control logic
* Hardware actuation

---

# 🔄 Complete Data Flow

```text
                 HISTORICAL INTELLIGENCE
                         │
                         ▼
                Meteorological Data
                         │
                         +
                  Astronomical Data
                         │
                         ▼
                  Machine Learning
                         │
                         ▼
                 Rainfall Intelligence
                         │
                         ▼
                   GROUND REALITY
                         │
                         ▼
                  Soil / Environment
                         │
                         ▼
                       Sensors
                         │
                         ▼
                       ESP32
                         │
                 ┌───────┴───────┐
                 ▼               ▼
           Web Interface    Irrigation System
                 │               │
                 └───────┬───────┘
                         ▼
                  Smart Agriculture
```

---

# ⚡ ESP32 and IoT Layer

The ESP32 forms the bridge between the physical environment and the software system.

Its documented responsibilities are:

1. Read sensor/environmental information.
2. Process incoming readings.
3. Establish network communication.
4. Exchange information with the web interface.
5. Control the irrigation mechanism.
6. Demonstrate physical actuation.

The controller workflow is:

```text
Sensor Input
     ↓
ESP32
     ↓
Read / Process
     ↓
Network Communication
     ↓
Web Interface
     ↓
Control Decision
     ↓
Actuator
```

---

# 🌐 Web Interface

A working web-host interface was demonstrated during the Phase 2 presentation.

Its intended role is to:

* Display system information
* Receive or reflect sensor information
* Provide an interface for irrigation control
* Communicate with the ESP32
* Demonstrate remote interaction with the physical system

Conceptually:

```text
                   WEB HOST
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
          Monitor           Control
             │                 │
             └────────┬────────┘
                      ▼
                    ESP32
                      │
                      ▼
                  Irrigation
```

The original documentation also anticipates web dashboards and REST APIs for broader deployment.

---

# 💧 Irrigation Control

The demonstrated irrigation flow is:

```text
Soil Condition
      ↓
Sensor Reading
      ↓
ESP32
      ↓
Control Logic
      ↓
Irrigation Actuator
      ↓
Water ON / OFF
```

A future integrated decision engine could combine rainfall intelligence with ground conditions:

```text
       Rainfall Prediction
               +
          Soil Condition
               +
       Environmental Data
               ↓
       Irrigation Decision
               ↓
         ESP32 Controller
               ↓
          Water Control
```

---

# ⚙️ Installation

## Prerequisites

For Phase 1, the supplied documentation specifies:

* **Python 3.9+**
* **8 GB RAM minimum**
* **16 GB RAM recommended**
* Sufficient storage for historical datasets

The IoT phase additionally requires the demonstrated ESP32, sensor setup, network connectivity, irrigation hardware, and suitable power supply.

## 1. Clone the Repository

```bash
git clone https://github.com/aiat-college/sdml23-project12.git
or 
git clone https://github.com/ayush-jena-721/Intelligent_Agro_Management_System.git
cd sdml23-project12
cd Intelligent_Agro_Management_System
```

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Python Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> The supplied documentation describes a relatively large dependency environment. Installation requirements may therefore vary depending on which project components are being executed.

---

# ▶️ Usage

## Phase 1 — Verify the Dataset

Run the NetCDF inspection utility:

```bash
python src/pipelines/verifing_variables.py
```

## Build the Processed Dataset

Using the Python module:

```bash
python -m src.pipelines.build_dataset
```

Alternatively:

```bash
python src/pipelines/build_dataset.py
```

The documented processing pipeline is:

```text
Load Panchangam
      ↓
Find rainfall data
      ↓
Load rainfall
      ↓
Create temporal features
      ↓
Create target
      ↓
Merge data
      ↓
Validate
      ↓
Save Parquet
```

---

# 📊 Loading Processed Data

A processed dataset can be loaded using Pandas:

```python
import pandas as pd

df = pd.read_parquet(
    "data/processed/dataset_year=2010.parquet"
)

print(df.head())
print(df.info())
```

Check dataset dimensions and columns:

```python
print("Rows:", len(df))
print("Columns:", df.columns.tolist())
```

Inspect rainfall:

```python
print(df["rainfall"].describe())
```

Inspect the T+2 target:

```python
print(df["rain_t2"].value_counts())
```

---

# 🌧️ Rainfall Analysis Example

Daily rainfall:

```python
daily_rainfall = (
    df.groupby("date")["rainfall"]
      .mean()
)

print("Mean rainfall:", daily_rainfall.mean())
print("Maximum rainfall:", daily_rainfall.max())
```

Monthly rainfall analysis:

```python
monthly = (
    df.groupby("month")["rainfall"]
      .mean()
)

print(monthly)
```

---

# 🔬 Model Training

The documented Phase 1 architecture uses **XGBoost** as the principal baseline model.

The training workflow includes:

* Train/test splitting
* Feature normalization
* Model fitting
* Prediction
* Error evaluation
* Rainfall-occurrence evaluation

The Phase 1 documentation also describes time-series-aware validation and model selection using mean absolute error for its documented regression experiments.

When the training module is configured for execution:

```bash
python -m src.pipelines.train_classifier
```

> The supplied documentation presents this as the documented training entry point; exact execution depends on the state of the corresponding implementation and configuration.

---

# 🔌 Phase 2 — IoT Usage

The demonstrated IoT workflow is:

### Step 1 — Power the Hardware

Power the ESP32 and sensor setup.

### Step 2 — Connect to the Network

Connect the ESP32 to its configured network.

### Step 3 — Initialize Sensors

Initialize the sensor interface and begin collecting measurements.

### Step 4 — Read Ground Conditions

Collect the soil/ground-condition reading.

### Step 5 — Communicate

Transmit or expose the information through the IoT/web layer.

### Step 6 — Open the Web Interface

Access the demonstrated web-host interface.

### Step 7 — Monitor and Control

Observe system information and interact with the irrigation control interface.

### Step 8 — Verify Physical Response

Confirm that the irrigation mechanism responds correctly.

---

# 🧪 Demonstration

The Phase 2 prototype successfully demonstrated:

| Component                          | Status                      |
| ---------------------------------- | --------------------------- |
| Soil / ground-condition monitoring | ✅ Demonstrated              |
| ESP32                              | ✅ Working                   |
| IoT communication                  | ✅ Demonstrated              |
| Web host                           | ✅ Working                   |
| Web-based interaction              | ✅ Demonstrated              |
| Irrigation mechanism               | ✅ Demonstrated              |
| Physical end-to-end prototype      | ✅ Successfully demonstrated |

The key achievement is the connection:

```text
Software
   ↕
Network
   ↕
ESP32
   ↕
Physical Environment
   ↕
Irrigation System
```

This makes the project a working **IoT proof-of-concept**, rather than only a theoretical architecture.

---

# 📈 Results

## Phase 1

The Phase 1 documentation reports:

* Proof-of-concept validation
* Successful dataset integration
* Successful modelling approach
* Seasonal rainfall pattern capture
* Observed astronomical correlations
* Better prediction stability compared with reported random baselines
* Improved detection of heavy-rainfall days
* Useful signals from astronomical features

The hybrid approach established a foundation for further smart-agriculture applications.

## Phase 2

Phase 2 provides a different form of validation: **physical implementation**.

Major achievements include:

```text
Soil Data
    │
    ├──────────────┐
    ▼              ▼
  ESP32         Web Host
    │              │
    └──────┬───────┘
           ▼
   Irrigation Control
           │
           ▼
   Physical Response
```

The demonstrated system therefore progressed from software experimentation to physical IoT operation.

---

# 🧪 Testing

Testing covers three major areas.

## Software Testing

* Data loading
* Date normalization
* Dataset validation
* Feature generation
* Model evaluation

## IoT Testing

* Sensor reading
* ESP32 operation
* Network communication
* Web-host connectivity
* Control interaction

## Hardware Testing

* Physical irrigation response
* Actuator operation
* Water-flow response
* End-to-end operation

---

# 🗂️ Project Structure

The original Phase 1 repository is organized as follows:

```text
sdml23-project12/
│
├── src/
│   ├── features/
│   │   ├── panchangam_features.py
│   │   ├── rainfall_lags.py
│   │   ├── rolling_stats.py
│   │   └── seasonal.py
│   │
│   ├── ingestion/
│   │   ├── imd_rainfall.py
│   │   └── panchangam.py
│   │
│   ├── models/
│   │   ├── rf_baseline.py
│   │   └── xgb_classifier.py
│   │
│   ├── pipelines/
│   │   ├── build_dataset.py
│   │   ├── train_classifier.py
│   │   └── verifing_variables.py
│   │
│   ├── preprocessing/
│   │   └── sanity.py
│   │
│   ├── split/
│   │   └── temporal.py
│   │
│   ├── targets/
│   │   └── rain_t2_binary.py
│   │
│   └── utils/
│       └── logger.py
│
├── schemas/
│   ├── dataset_schema.py
│   └── grid.py
│
├── scripts/
│   ├── build_dataset.sh
│   └── train.sh
│
├── configs/
│   ├── paths.yaml
│   ├── split.yaml
│   └── thresholds.yaml
│
├── data/
│   ├── raw/
│   │   └── imd/
│   ├── panchangam/
│   └── processed/
│
├── README.md
├── requirements.txt
├── SRC_DOCUMENTATION.md
├── REQUIREMENTS_ANALYSIS.md
└── COMPREHENSIVE_DOCUMENTATION.md
```

For the combined final-year implementation, the IoT portion can be organized separately:

```text
iot/
├── esp32/
│   ├── firmware/
│   └── configuration/
│
├── web/
│   ├── frontend/
│   └── backend/
│
├── sensors/
│   └── sensor_configuration/
│
└── irrigation/
    └── control_logic/
```

---

# 🧰 Technology Stack

## Artificial Intelligence

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost

## Astronomy

* Skyfield
* PyJHora
* Swiss Ephemeris
* JPL Ephemeris

## Data

* Open-Meteo
* IMD data
* CSV
* JSONL
* NetCDF
* Apache Parquet
* PyArrow

## Visualization

* Matplotlib
* Seaborn
* Plotly
* PyDeck

## Web

* Streamlit
* FastAPI / Starlette
* Uvicorn

## IoT

* ESP32
* Environmental/soil sensors
* Network communication
* Web-host interface
* Irrigation actuator/control hardware

---

# ✅ Implementation Status

## Phase 1

| Component                          | Status |
| ---------------------------------- | ------ |
| Historical weather data processing | ✅      |
| Astronomical data generation       | ✅      |
| Panchangam generation              | ✅      |
| Feature engineering                | ✅      |
| Dataset integration                | ✅      |
| Rainfall target generation         | ✅      |
| XGBoost experimentation            | ✅      |
| Phase 1 feasibility validation     | ✅      |

## Phase 2

| Component                        | Status |
| -------------------------------- | ------ |
| Ground/soil-condition collection | ✅      |
| IoT architecture                 | ✅      |
| ESP32 integration                | ✅      |
| Sensor-to-controller workflow    | ✅      |
| Web host                         | ✅      |
| Web/IoT interaction              | ✅      |
| Irrigation control prototype     | ✅      |
| Physical demonstration           | ✅      |

## Future

| Component                          | Status |
| ---------------------------------- | ------ |
| AI + IoT unified decision engine   | 🚧     |
| Automated weather-aware irrigation | 🚧     |
| Real-time prediction API           | 🚧     |
| Advanced dashboard                 | 🚧     |
| LSTM/CNN models                    | 🚧     |
| Satellite integration              | 🚧     |
| Crop recommendation                | 🚧     |
| Plant disease detection            | 🚧     |
| Large-scale field deployment       | 🚧     |

---

# 🏆 Advantages

### 1. Hybrid Architecture

Combines:

* Weather data
* Astronomical information
* Machine learning
* Ground-level sensing
* IoT
* Web technology

### 2. Real-World Validation

Phase 2 demonstrates actual hardware instead of remaining entirely theoretical.

### 3. Modular Design

The system can evolve independently across:

```text
Data
ML
IoT
Web
Hardware
```

### 4. Water Management Potential

The irrigation layer provides a foundation for reducing unnecessary watering.

### 5. Scalable Architecture

The proof-of-concept can serve as a foundation for larger agricultural deployments.

---

# ⚠️ Limitations

MeghDristi is currently a **research and proof-of-concept project**.

## Phase 1 Limitations

* Historical data does not guarantee future forecasting accuracy.
* Rainfall behaviour varies geographically.
* Astronomical correlations require further scientific validation.
* Larger datasets and controlled experiments are required.
* Production forecasting requires stronger validation.

## Phase 2 Limitations

* The demonstrated system is a mini prototype.
* Sensor coverage is limited.
* The setup represents a controlled demonstration environment rather than a full agricultural field.
* Large-scale deployment requires robust power, networking, waterproofing, calibration, and maintenance.
* Irrigation decisions should not depend solely on one sensor or one prediction source.

---

# 🚀 Future Scope

## Phase 3 — Intelligent Agricultural Platform

The next major direction is to integrate AI and IoT into a unified decision system.

```text
Rainfall Prediction
        +
Soil Moisture
        +
Temperature
        +
Humidity
        +
Rain Forecast
        ↓
Irrigation Decision
```

## Advanced Machine Learning

Potential future models include:

* LSTM
* CNN
* Ensemble learning
* Hyperparameter optimization
* Temporal deep learning

## Smart Irrigation

A future decision engine could use logic such as:

```text
IF soil is dry
AND rainfall probability is low
THEN irrigate

IF soil is sufficiently wet
OR significant rainfall is expected
THEN reduce/stop irrigation
```

These rules should ultimately be based on **calibrated sensor measurements and validated agricultural thresholds**, rather than arbitrary values.

## Real-Time Dashboard

A future dashboard could combine:

* Soil condition
* Temperature
* Humidity
* Rain probability
* Rainfall prediction
* Pump status
* Irrigation controls

## Crop Recommendation

Future versions could consider:

* Crop type
* Soil condition
* Rainfall forecast
* Temperature
* Humidity
* Seasonal conditions

## Plant Disease Detection

Computer vision could eventually provide:

```text
Plant Image
     ↓
CNN
     ↓
Disease Detection
     ↓
Disease Classification
     ↓
Recommended Action
```

---

# 📊 Success Criteria

## Machine Learning

Relevant evaluation metrics include:

* Accuracy
* Precision
* Recall
* F1-score
* ROC-AUC
* PR-AUC
* MAE
* RMSE

## Data Quality

Important checks include:

* Missingness
* Temporal coverage
* Spatial coverage
* Feature variance
* Class balance

## IoT

Phase 2 can be evaluated using:

* Sensor-reading reliability
* ESP32 connectivity
* Web-host availability
* Command-response latency
* Actuator response
* Irrigation ON/OFF reliability
* End-to-end operation

---

# 🔐 Security Considerations

Production deployment should protect credentials and device communication.

## Credentials

Never hard-code:

* Wi-Fi passwords
* API keys
* Cloud credentials
* Database credentials

Use environment variables or secure configuration instead.

The project documentation specifically recommends `.env`-style credential management and avoiding committed secrets.

## IoT Security

A production implementation should consider:

* Authenticated device communication
* Secure API endpoints
* Access control
* Encrypted communication
* Device authentication
* Secure firmware updates

---

# 🧭 Project Roadmap

```text
                      MEGHDRISTI
                         │
                         ▼
              ┌─────────────────────┐
              │       PHASE 1       │
              │ Weather Intelligence│
              └──────────┬──────────┘
                         │
                         ▼
                   Historical Data
                         │
                         ▼
                  Astronomical Data
                         │
                         ▼
                    Machine ML
                         │
                         ▼
                  Rainfall Prediction
                         │
                         ▼
              ┌─────────────────────┐
              │       PHASE 2       │
              │   IoT Agriculture   │
              └──────────┬──────────┘
                         │
                         ▼
                    Soil / Ground
                       Sensors
                         │
                         ▼
                        ESP32
                         │
                 ┌───────┴───────┐
                 ▼               ▼
             Web Host        Irrigation
                 │               │
                 └───────┬───────┘
                         ▼
                Working Demonstration
                         │
                         ▼
              ┌─────────────────────┐
              │       PHASE 3       │
              │ Intelligent Farming │
              └──────────┬──────────┘
                         │
                         ▼
                  AI + IoT Integration
                         │
                         ▼
                   Automated Decisions
                         │
                         ▼
                  Smart Agriculture
```

---

# 👥 Project Team

### Final Year Project

* **Ayush Jena**
* **Yogalakshmi**

The Phase 1 documentation identifies both as project contributors.

---

# 📚 Documentation

The supplied project documentation references:

| File                             | Description                        |
| -------------------------------- | ---------------------------------- |
| `README.md`                      | Main project documentation         |
| `SRC_DOCUMENTATION.md`           | Source-code documentation          |
| `REQUIREMENTS_ANALYSIS.md`       | Dependency and technology analysis |
| `COMPREHENSIVE_DOCUMENTATION.md` | Extended technical documentation   |
| `MeghDristi-Phase-1.pdf`         | Phase 1 project presentation       |

The requirements documentation describes a broad dependency environment covering data processing, machine learning, astronomy, visualization, web, validation, and infrastructure.

---

# 📜 License

No specific license is currently defined in the supplied project documentation.

A suitable **open-source or academic-project license** should be added before public distribution.

---

# 🙏 Acknowledgements

The project acknowledges the use of:

* Indian Meteorological Department data
* Open-Meteo weather services
* Astronomical computation libraries
* Open-source machine-learning frameworks
* ESP32 and IoT ecosystem
* Open-source software and developer communities

---

# 🏁 Conclusion

MeghDristi began as a **hybrid AI-based rainfall prediction project** combining meteorological and astronomical information.

Phase 1 established the computational foundation through:

* Weather-data collection
* Astronomical-data generation
* Predictive feature engineering
* Machine-learning dataset construction
* XGBoost experimentation
* Feasibility validation

Phase 2 extended this foundation into the physical world through:

* Ground/soil-condition monitoring
* ESP32-based IoT control
* Web-host interaction
* Irrigation actuation
* Physical end-to-end demonstration

The project's evolution can therefore be summarized as:

```text
Data → Model
```

becoming:

```text
Data → Intelligence → Physical Environment → IoT → Control
```

The long-term vision is an intelligent agricultural ecosystem combining:

```text
🌦️ Weather Intelligence
        +
🌙 Astronomical Research
        +
🤖 Machine Learning
        +
🌱 Ground / Soil Monitoring
        +
📡 IoT
        +
🌐 Web Technology
        +
💧 Automated Irrigation
        │
        ▼
🌾 SMART AGRICULTURE
```

> **MeghDristi — from understanding the sky to responding to the ground.**

---

## Project Information

| Field                     | Details                                         |
| ------------------------- | ----------------------------------------------- |
| **Project**               | MeghDristi                                      |
| **Type**                  | Final Year Project                              |
| **Domain**                | AI · Machine Learning · IoT · Smart Agriculture |
| **Phase 1**               | Rainfall Intelligence                           |
| **Phase 2**               | IoT Irrigation                                  |
| **Current Status**        | ✅ Working Proof of Concept                      |
| **Phase 2 Demonstration** | ✅ Successfully Completed                        |
| **ESP32**                 | ✅ Successfully Demonstrated                     |
| **Web Host**              | ✅ Successfully Demonstrated                     |
| **Irrigation Prototype**  | ✅ Successfully Demonstrated                     |

The supplied project documentation describes the current implementation as a successfully demonstrated proof of concept across both software and hardware layers.
