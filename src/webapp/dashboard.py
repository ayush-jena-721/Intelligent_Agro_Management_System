# import sys
# from pathlib import Path
# import streamlit as st
# import pandas as pd
# from pydantic import BaseModel

# # ---------------- PATH SETUP ----------------
# BASE_DIR = Path(__file__).resolve().parents[2]
# sys.path.append(str(BASE_DIR / "src"))

# # ---------------- IMPORTS ----------------
# from webapp.feature_builder import build_features, FEATURE_COLUMNS
# from webapp.weather_fetcher import fetch_current_weather
# from webapp.panchang_loader import load_panchang, get_panchang_for_date, merge_with_weather
# from webapp.predictor import load_model, predict_rain
# from webapp.panchang_mapper import map_panchang_names

# # ---------------- CONFIG ----------------
# st.set_page_config(page_title="MeghDristi", layout="wide")

# # ---------------- UI STYLE ----------------
# st.markdown("""
# <style>

# /* Floating Button */
# .chat-button {
#     position: fixed;
#     bottom: 25px;
#     right: 25px;
#     background: #00c3ff;
#     color: white;
#     border-radius: 50%;
#     width: 65px;
#     height: 65px;
#     text-align: center;
#     font-size: 30px;
#     line-height: 65px;
#     cursor: pointer;
#     box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
#     z-index: 999;
# }

# /* Chat Box */
# .chat-box {
#     position: fixed;
#     bottom: 100px;
#     right: 25px;
#     width: 320px;
#     height: 420px;
#     background: rgba(0,0,0,0.85);
#     border-radius: 15px;
#     padding: 15px;
#     display: none;
#     flex-direction: column;
#     z-index: 999;
# }

# /* Chat Header */
# .chat-header {
#     font-weight: bold;
#     margin-bottom: 10px;
# }

# /* Chat Messages */
# .chat-content {
#     flex-grow: 1;
#     overflow-y: auto;
#     font-size: 14px;
# }

# /* Input */
# .chat-input {
#     width: 100%;
#     padding: 8px;
#     margin-top: 10px;
#     border-radius: 8px;
#     border: none;
# }

# </style>
# """, unsafe_allow_html=True)

# st.markdown("""
# <style>
# .block-container {
#     padding: 2rem 3rem;
# }

# .main {
#     background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
# }

# .glass {
#     background: rgba(255,255,255,0.07);
#     backdrop-filter: blur(14px);
#     border-radius: 18px;
#     padding: 25px;
#     margin-bottom: 25px;
#     border: 1px solid rgba(255,255,255,0.15);
# }

# h2, h3 {
#     margin-bottom: 10px;
# }
# </style>
# """, unsafe_allow_html=True)

# st.title("🌾 MeghDristi – Rainfall prediction (Panchangam) & Smart Rain Based Irrigation System")

# CUTOFF_DATE = pd.Timestamp("2026-01-01")

# # ---------------- SIDEBAR ----------------
# st.sidebar.header("📍 User Input")

# lat = st.sidebar.number_input("Latitude", value=12.02)
# lon = st.sidebar.number_input("Longitude", value=79.56)
# use_current_time = st.sidebar.checkbox("Use Current Time", value=True)

# if use_current_time:
#     selected_datetime = pd.Timestamp.now()
# else:
#     date_input = st.sidebar.date_input("Select Date")
#     time_input = st.sidebar.time_input("Select Time")
#     selected_datetime = pd.Timestamp.combine(date_input, time_input)

# # ---------------- MODEL ----------------
# @st.cache_resource
# def get_model():
#     return load_model()

# model = get_model()

# # ---------------- DATA ----------------
# @st.cache_data
# def load_historical():
#     df = pd.read_csv(BASE_DIR / "data/processed/weather_features.csv")
#     df["date"] = pd.to_datetime(df["date"], errors="coerce")
#     df = df.rename(columns={"rainfall": "precipitation"})
#     return df

# hist_df = load_historical()

# def get_nearest_row(df, selected_datetime):
#     df = df.sort_values("date").drop_duplicates("date")
#     idx = (df["date"] - selected_datetime).abs().idxmin()
#     return df.loc[[idx]].copy()

# # ---------------- FUTURE PRED ----------------
# def predict_next_days(model, base_df, days=5):
#     future = []
#     temp = base_df.copy()

#     for _ in range(days):
#         temp["date"] += pd.Timedelta(days=1)

#         features = build_features(temp, True)
#         features = features.reindex(columns=FEATURE_COLUMNS, fill_value=0)

#         pred = float(predict_rain(model, features)[0])
#         pred = max(0, pred)

#         future.append({"date": temp["date"].iloc[-1], "rain": pred})
#         temp["precipitation"] = pred

#     return pd.DataFrame(future)

# # ---------------- ADVISORY ----------------
# def generate_advisory(temp, humidity, rain):
#     if rain > 0.7:
#         return "🚫 Avoid spraying. Ensure drainage."
#     elif rain > 0.3:
#         return "🌱 Good for sowing."
#     elif temp > 35:
#         return "🔥 Increase irrigation."
#     elif humidity < 30:
#         return "🌾 Mulching recommended."
#     return "✅ Conditions stable."

# # ---------------- PYDANTIC AI ----------------
# class FarmResponse(BaseModel):
#     rainfall: float
#     irrigation: str
#     advisory: str

# def generate_ai_response(prediction, decision, advisory):
#     return FarmResponse(
#         rainfall=prediction,
#         irrigation=decision,
#         advisory=advisory
#     )

# def get_sensor_data():
#     return {
#         "soil_moisture": 32,   # %
#         "soil_temp": 29,       # °C
#         "water_level": 68,     # %
#         "pump_status": "OFF"
#     }

# def iot_decision_logic(sensor, prediction):
#     if sensor["soil_moisture"] < 30 and prediction < 0.3:
#         return "🚿 Pump ON (Dry soil + No rain expected)"
#     elif prediction > 0.6:
#         return "🚫 Pump OFF (Rain incoming)"
#     elif sensor["water_level"] < 20:
#         return "⚠️ Low tank level - conserve water"
#     return "✅ System Stable"

# # ---------------- MAIN ----------------
# if st.button(" Predict Rainfall"):

#     try:
#         # ---------- DATA SOURCE ----------
#         if selected_datetime < CUTOFF_DATE:
#             df = get_nearest_row(hist_df, selected_datetime)
#         else:
#             df = fetch_current_weather(lat, lon)

#         panch = load_panchang()
#         panch_row = get_panchang_for_date(panch, selected_datetime)

#         df = merge_with_weather(df, panch_row)
#         df = map_panchang_names(df)

#         latest = df.iloc[-1]

#         # ---------- PREDICTION ----------
#         features = build_features(df, True)
#         features = features.reindex(columns=FEATURE_COLUMNS, fill_value=0)

#         prediction = float(predict_rain(model, features)[0])
#         prediction = max(0, prediction)

#         # ---------- IRRIGATION ----------
#         soil = latest.get("humidity", 50)

#         if prediction > 0.7:
#             decision = "🚫 Skip irrigation"
#         elif prediction > 0.3:
#             decision = "💧 Light irrigation"
#         elif soil < 40:
#             decision = "🚿 Immediate irrigation"
#         else:
#             decision = "🌱 Normal watering"

#         # ---------- ADVISORY ----------
#         advisory = generate_advisory(
#             latest.get("temperature_2m", 0),
#             latest.get("humidity", 0),
#             prediction
#         )
#         #========== AI EXPLAINER ========================
#         def ai_explainer(prediction, latest):
#             tithi = latest.get("tithi", "unknown")
#             nakshatra = latest.get("nakshatra", "unknown")
#             vara = latest.get("vara", "unknown")

#             explanation = f"""
#         🌧 Rainfall Prediction: {prediction:.2f} mm

#         📊 AI Insight:
#         The system analyzes historical rainfall, humidity, and seasonal cycles 
#         to estimate future rainfall patterns.

#         🌙 Panchang Influence:
#         • Tithi ({tithi}) influences moisture cycles.
#         • Nakshatra ({nakshatra}) is linked with atmospheric behavior.
#         • Vara ({vara}) represents weekday planetary effects.

#         🔗 Combined Intelligence:
#         Modern ML + Traditional Panchang = Better agricultural timing.

#         🚿 Suggestion:
#         {'Irrigation not required' if prediction > 5 else 'Irrigation recommended'}

#         🌾 This is not just prediction — it's decision intelligence.
#         """
#             return explanation




#         # ================= DASHBOARD =================
#         st.markdown("## 🌾 Dashboard Overview")

#         col1, col2, col3 = st.columns(3, gap="large")

#         col1.markdown(f'<div class="glass"><h3>🌧 Rainfall</h3><h1>{prediction:.2f} mm</h1></div>', unsafe_allow_html=True)
#         col2.markdown(f'<div class="glass"><h3>🌡 Temperature</h3><h1>{latest.get("temperature_2m",0):.1f}°C</h1></div>', unsafe_allow_html=True)
#         col3.markdown(f'<div class="glass"><h3>💧 Humidity</h3><h1>{latest.get("humidity",0):.1f}%</h1></div>', unsafe_allow_html=True)

#         # ================= DECISION =================
#         st.markdown("## 🚿 Farm Decision Support")

#         col1, col2 = st.columns(2, gap="large")

#         col1.markdown(f'<div class="glass"><h3> Irrigation</h3><p>{decision}</p></div>', unsafe_allow_html=True)
#         col2.markdown(f'<div class="glass"><h3> Advisory</h3><p>{advisory}</p></div>', unsafe_allow_html=True)

#         # ================= FORECAST =================
#         future_df = predict_next_days(model, df.tail(1))

#         st.markdown("## 📊 Insights & Trends")

#         st.markdown("### 🌧 Rainfall Forecast")
#         st.line_chart(future_df.set_index("date"), height=300)

#         if "humidity" in df.columns:
#             st.markdown("### 💧 Rain vs Humidity")
#             clean_df = df[["date", "humidity", "precipitation"]].dropna().tail(24)
#             st.line_chart(clean_df.set_index("date"), height=300)

#         future_df["trend"] = future_df["rain"].diff()

#         st.markdown("### ⚖️ Rain Trend")
#         st.area_chart(future_df.set_index("date")[["trend"]], height=250)

#         # ================= IoT SENSOR SECTION =================
#         st.markdown("## 📡 IoT Sensor Intelligence")

#         sensor = get_sensor_data()
#         iot_status = iot_decision_logic(sensor, prediction)

#         c1, c2, c3, c4 = st.columns(4, gap="large")

#         c1.markdown(f'''
#         <div class="glass">
#         <h4>🌱 Soil Moisture</h4>
#         <h2>{sensor["soil_moisture"]}%</h2>
#         </div>''', unsafe_allow_html=True)

#         c2.markdown(f'''
#         <div class="glass">
#         <h4>🌡 Soil Temp</h4>
#         <h2>{sensor["soil_temp"]}°C</h2>
#         </div>''', unsafe_allow_html=True)

#         c3.markdown(f'''
#         <div class="glass">
#         <h4>💧 Water Level</h4>
#         <h2>{sensor["water_level"]}%</h2>
#         </div>''', unsafe_allow_html=True)

#         c4.markdown(f'''
#         <div class="glass">
#         <h4>🚿 Pump</h4>
#         <h2>{sensor["pump_status"]}</h2>
#         </div>''', unsafe_allow_html=True)

#         # ================= LOGIC PANEL =================
#         st.markdown("### ⚙️ Automation Logic")

#         st.markdown(f'''
#         <div class="glass">
#         <p>{iot_status}</p>
#         </div>
#         ''', unsafe_allow_html=True)

#         # ================= PANCHANG =================
#         st.markdown("## 🪐 Panchang Insights")

#         col1, col2, col3, col4 = st.columns(4)

#         data = [
#             ("Tithi", latest.get("tithi","")),
#             ("Nakshatra", latest.get("nakshatra","")),
#             ("Vara", latest.get("vara","")),
#             # ("Yoga", latest.get("yoga","")),
#             # ("Karana", latest.get("karana","")),
#             ("Moon", latest.get("moon_phase",""))
#         ]

#         for col, (title, val) in zip([col1,col2,col3,col4], data):
#             col.markdown(f'<div class="glass"><h4>{title}</h4><p>{val}</p></div>', unsafe_allow_html=True)



#         # # ================= AI =================
#         # st.markdown("## 🤖 AI Farm Assistant")

#         # response = generate_ai_response(prediction, decision, advisory)
#         # st.json(response.dict())

#         # ================= FOOTER =================
#         st.markdown("---")
#         st.markdown("""
#         <div style='text-align:center; opacity:0.6; padding:20px'>
#             <p>🌾 MeghDristi Smart Agriculture System</p>
#             <p>Developed by Yogalakshmi & Ayush Jena</p>
#             <p>© 2026 All Rights Reserved</p>
#         </div>
#         """, unsafe_allow_html=True)

#     except Exception as e:
#         st.error(f"❌ Error: {e}")




import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import requests
from pydantic import BaseModel
import time

# ---------------- PATH SETUP ----------------
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR / "src"))

# ---------------- IMPORTS ----------------
from webapp.feature_builder import build_features, FEATURE_COLUMNS
from webapp.weather_fetcher import fetch_current_weather
from webapp.panchang_loader import load_panchang, get_panchang_for_date, merge_with_weather
from webapp.predictor import load_model, predict_rain
from webapp.panchang_mapper import map_panchang_names

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="MeghDristi | Smart Agriculture IoT Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- AUTO REFRESH SETUP ----------------
# Initialize session state for auto-refresh
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

# Auto-refresh every 5 seconds using JavaScript
st.markdown("""
<script>
    // Auto-refresh every 5 seconds
    setTimeout(function(){
        window.location.reload();
    }, 5000);
</script>
""", unsafe_allow_html=True)

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');

* {
    font-family: 'Rajdhani', sans-serif;
}

.block-container {
    padding: 1rem 2rem;
    max-width: 100%;
}

.main {
    background: linear-gradient(135deg, #0a1628 0%, #1a2a4a 50%, #0f2847 100%);
    color: #ffffff;
}

/* Glassmorphism Cards */
.glass {
    background: rgba(16, 30, 60, 0.6);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
    border: 1px solid rgba(0, 195, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}

.glass:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 195, 255, 0.15);
    border-color: rgba(0, 195, 255, 0.4);
}

/* Sensor Cards - Dynamic Colors */
.sensor-card {
    background: linear-gradient(135deg, rgba(0, 195, 255, 0.1) 0%, rgba(0, 100, 200, 0.1) 100%);
    border-left: 4px solid #00c3ff;
}

.sensor-critical {
    background: linear-gradient(135deg, rgba(255, 50, 50, 0.15) 0%, rgba(200, 0, 0, 0.1) 100%);
    border-left: 4px solid #ff3333;
    animation: pulse-red 2s infinite;
}

.sensor-warning {
    background: linear-gradient(135deg, rgba(255, 200, 0, 0.15) 0%, rgba(200, 150, 0, 0.1) 100%);
    border-left: 4px solid #ffc800;
}

.sensor-optimal {
    background: linear-gradient(135deg, rgba(0, 255, 150, 0.15) 0%, rgba(0, 200, 100, 0.1) 100%);
    border-left: 4px solid #00ff96;
}

@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 20px rgba(255, 51, 51, 0.3); }
    50% { box-shadow: 0 0 40px rgba(255, 51, 51, 0.6); }
}

/* Typography */
h1 {
    font-family: 'Orbitron', sans-serif;
    background: linear-gradient(90deg, #00c3ff, #0077ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

h2, h3 {
    font-family: 'Orbitron', sans-serif;
    color: #00c3ff;
    margin-bottom: 15px;
    font-size: 1.3rem;
    text-transform: uppercase;
    letter-spacing: 2px;
}

h4 {
    color: #88ccff;
    font-size: 0.9rem;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Big Numbers */
.metric-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(180deg, #ffffff 0%, #00c3ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}

.metric-unit {
    font-size: 1rem;
    color: #88ccff;
    margin-left: 5px;
}

/* Status Indicators */
.status-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.status-online {
    background: rgba(0, 255, 150, 0.2);
    color: #00ff96;
    border: 1px solid #00ff96;
}

.status-offline {
    background: rgba(255, 50, 50, 0.2);
    color: #ff3333;
    border: 1px solid #ff3333;
}

/* Connection Status Bar */
.connection-bar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #00c3ff, #0077ff, #00c3ff);
    background-size: 200% 100%;
    animation: shimmer 2s infinite;
    z-index: 1000;
}

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

/* Last Updated Timestamp */
.timestamp {
    text-align: right;
    color: #88ccff;
    font-size: 0.8rem;
    margin-bottom: 20px;
    opacity: 0.8;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.2);
}

::-webkit-scrollbar-thumb {
    background: #00c3ff;
    border-radius: 4px;
}

/* Responsive Grid */
@media (max-width: 768px) {
    .metric-value {
        font-size: 2rem;
    }
    h1 {
        font-size: 1.5rem;
    }
}

/* Chart Container */
.chart-container {
    background: rgba(16, 30, 60, 0.4);
    border-radius: 15px;
    padding: 20px;
    margin-top: 20px;
}

/* IoT Section Glow */
.iot-section {
    position: relative;
}

.iot-section::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, #00c3ff, #0077ff, #00c3ff);
    border-radius: 22px;
    z-index: -1;
    opacity: 0.3;
    filter: blur(10px);
}

/* Pump Animation */
.pump-active {
    animation: pump-pulse 1s infinite;
}

@keyframes pump-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

/* Footer */
.footer {
    text-align: center;
    padding: 30px;
    margin-top: 40px;
    border-top: 1px solid rgba(0, 195, 255, 0.2);
    color: #88ccff;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# Connection status bar
st.markdown('<div class="connection-bar"></div>', unsafe_allow_html=True)

# Header
st.markdown("""
<h1> 🌾 MeghDristi</h1>
<p style='text-align:center; color:#88ccff; font-size:1.1rem; margin-bottom:30px;'>
    AI-Powered Rainfall Prediction & Smart IoT Irrigation System
</p>
""", unsafe_allow_html=True)

# Last updated timestamp
current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f'<div class="timestamp">🔄 Last Updated: {current_time} | Auto-refresh: 5s</div>', unsafe_allow_html=True)

CUTOFF_DATE = pd.Timestamp("2026-01-01")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; margin-bottom:20px;'>
        <h3 style='color:#00c3ff;'>⚙️ Control Panel</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("📍 Location Settings")
    
    lat = st.number_input("Latitude", value=12.02, format="%.4f")
    lon = st.number_input("Longitude", value=79.56, format="%.4f")
    
    st.markdown("---")
    
    use_current_time = st.checkbox("Use Current Time", value=True)
    
    if use_current_time:
        selected_datetime = pd.Timestamp.now()
        st.info(f"🕐 {selected_datetime.strftime('%Y-%m-%d %H:%M')}")
    else:
        date_input = st.date_input("Select Date")
        time_input = st.time_input("Select Time")
        selected_datetime = pd.Timestamp.combine(date_input, time_input)
    
    st.markdown("---")
    
    # ESP32 Connection Status in Sidebar
    st.header("🔗 IoT Connection")
    ESP32_IP = "http://192.168.137.226/api"
    
    try:
        test_resp = requests.get(ESP32_IP, timeout=2)
        if test_resp.status_code == 200:
            st.markdown('<span class="status-badge status-online">● ESP32 Online</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-badge status-offline">● ESP32 Offline</span>', unsafe_allow_html=True)
    except:
        st.markdown('<span class="status-badge status-offline">● ESP32 Offline</span>', unsafe_allow_html=True)
    
    st.caption(f"IP: {ESP32_IP}")

# ---------------- MODEL ----------------
@st.cache_resource
def get_model():
    return load_model()

model = get_model()

# ---------------- DATA ----------------
@st.cache_data
def load_historical():
    df = pd.read_csv(BASE_DIR / "data/processed/weather_features.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.rename(columns={"rainfall": "precipitation"})
    return df

hist_df = load_historical()

def get_nearest_row(df, selected_datetime):
    df = df.sort_values("date").drop_duplicates("date")
    idx = (df["date"] - selected_datetime).abs().idxmin()
    return df.loc[[idx]].copy()

# ---------------- FUTURE PRED ----------------
def predict_next_days(model, base_df, days=5):
    future = []
    temp = base_df.copy()

    for _ in range(days):
        temp["date"] += pd.Timedelta(days=1)

        features = build_features(temp, True)
        features = features.reindex(columns=FEATURE_COLUMNS, fill_value=0)

        pred = float(predict_rain(model, features)[0])
        pred = max(0, pred)

        future.append({"date": temp["date"].iloc[-1], "rain": pred})
        temp["precipitation"] = pred

    return pd.DataFrame(future)

# ---------------- ADVISORY ----------------
def generate_advisory(temp, humidity, rain):
    if rain > 0.7:
        return "🚫 Avoid spraying. Ensure drainage."
    elif rain > 0.3:
        return "🌱 Good for sowing."
    elif temp > 35:
        return "🔥 Increase irrigation."
    elif humidity < 30:
        return "🌾 Mulching recommended."
    return "✅ Conditions stable."

# ---------------- PYDANTIC AI ----------------
class FarmResponse(BaseModel):
    rainfall: float
    irrigation: str
    advisory: str

def generate_ai_response(prediction, decision, advisory):
    return FarmResponse(
        rainfall=prediction,
        irrigation=decision,
        advisory=advisory
    )

# ---------------- IOT SENSOR FETCHER ----------------
def get_sensor_data():
    ESP32_IP = "http://192.168.137.226/api"
    
    try:
        res = requests.get(ESP32_IP, timeout=5)  # Increased timeout
        data = res.json()
        
        # FIXED: Handle both old and new key names for compatibility
        part1 = data.get("part1", data.get("plant1", 0))
        part2 = data.get("part2", data.get("plant2", 0))
        
        # Determine pump status
        pump_status = "OFF"
        if part1 < 30 or part2 < 30:
            pump_status = "ON"
        
        return {
            "soil_moisture": part1,
            "soil_moisture2": part2,
            "soil_temp": data.get("temperature", 0),
            "humidity": data.get("humidity", 0),
            "water_level": data.get("water_level", (part1 + part2) / 2),  # Fallback calculation
            "pump_status": data.get("pump_status", pump_status),
            "connection": "online",
            "raw_data": data
        }
    except Exception as e:
        st.warning(f"ESP32 Connection Failed: {e}")
        return {
            "soil_moisture": 0,
            "soil_moisture2": 0,
            "soil_temp": 0,
            "humidity": 0,
            "water_level": 0,
            "pump_status": "ERROR",
            "connection": "offline",
            "error": str(e)
        }

def get_sensor_card_class(value, optimal_min=40, optimal_max=70):
    """Return CSS class based on sensor value"""
    if value < optimal_min:
        return "sensor-critical"
    elif value > optimal_max:
        return "sensor-warning"
    return "sensor-optimal"

def iot_decision_logic(sensor, prediction):
    """Smart irrigation decision based on sensor data + weather prediction"""
    if sensor["connection"] == "offline":
        return "⚠️ Sensor Offline - Manual Mode"
    
    part1 = sensor["soil_moisture"]
    part2 = sensor["soil_moisture2"]
    avg_moisture = (part1 + part2) / 2
    
    if part1 < 20 or part2 < 20:
        return "🚨 CRITICAL: Immediate irrigation required!"
    elif avg_moisture < 30 and prediction < 0.3:
        return "🚿 Pump AUTO-ON: Dry soil + No rain expected"
    elif prediction > 0.7:
        return "🚫 Pump OFF: Heavy rain incoming"
    elif avg_moisture < 40:
        return "💧 Light irrigation recommended"
    elif avg_moisture > 60:
        return "✅ Soil optimal - No irrigation needed"
    return "🌱 Monitoring - Conditions stable"

# ================= MAIN DASHBOARD =================
if st.button("🌧️ Predict Rainfall", use_container_width=True):
    try:
        # ---------- DATA SOURCE ----------
        if selected_datetime < CUTOFF_DATE:
            df = get_nearest_row(hist_df, selected_datetime)
        else:
            df = fetch_current_weather(lat, lon)

        panch = load_panchang()
        panch_row = get_panchang_for_date(panch, selected_datetime)

        df = merge_with_weather(df, panch_row)
        df = map_panchang_names(df)

        latest = df.iloc[-1]

        # ---------- PREDICTION ----------
        features = build_features(df, True)
        features = features.reindex(columns=FEATURE_COLUMNS, fill_value=0)

        prediction = float(predict_rain(model, features)[0])
        prediction = max(0, prediction)

        # ---------- IRRIGATION ----------
        soil = latest.get("humidity", 50)

        if prediction > 0.7:
            decision = "🚫 Skip irrigation"
        elif prediction > 0.3:
            decision = "💧 Light irrigation"
        elif soil < 40:
            decision = "🚿 Immediate irrigation"
        else:
            decision = "🌱 Normal watering"

        # ---------- ADVISORY ----------
        advisory = generate_advisory(
            latest.get("temperature_2m", 0),
            latest.get("humidity", 0),
            prediction
        )

        # ================= WEATHER DASHBOARD =================
        st.markdown("## 🌤️ Weather Intelligence")
        
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        with col1:
            st.markdown(f'''
            <div class="glass">
                <h4> 🌧 Rainfall</h4>
                <div class="metric-value">{prediction:.1f}<span class="metric-unit">mm</span></div>
                <div style="margin-top:10px; color:{"#ff3333" if prediction > 10 else "#00ff96"}; font-size:0.9rem;">
                    {"Heavy Rain" if prediction > 10 else "Light Rain" if prediction > 0 else "No Rain"}
                </div>
            </div>''', unsafe_allow_html=True)
        
        with col2:
            temp_val = latest.get("temperature_2m", 0)
            st.markdown(f'''
            <div class="glass">
                <h4> 🌡 Temperature</h4>
                <div class="metric-value">{temp_val:.1f}<span class="metric-unit">°C</span></div>
                <div style="margin-top:10px; color:{"#ff3333" if temp_val > 35 else "#00ff96"}; font-size:0.9rem;">
                    {"Hot" if temp_val > 35 else "Cold" if temp_val < 15 else "Optimal"}
                </div>
            </div>''', unsafe_allow_html=True)
        
        with col3:
            hum_val = latest.get("humidity", 0)
            st.markdown(f'''
            <div class="glass">
                <h4> 💧 Humidity</h4>
                <div class="metric-value">{hum_val:.1f}<span class="metric-unit">%</span></div>
                <div style="margin-top:10px; color:{"#ffc800" if hum_val < 30 else "#00ff96"}; font-size:0.9rem;">
                    {"Dry" if hum_val < 30 else "Humid" if hum_val > 70 else "Optimal"}
                </div>
            </div>''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="glass">
                <h4>🌱 Irrigation</h4>
                <div style="font-size:1.2rem; color:#00c3ff; margin-top:10px;">{decision}</div>
                <div style="margin-top:15px; font-size:0.85rem; opacity:0.8;">{advisory}</div>
            </div>''', unsafe_allow_html=True)

        # ================= IoT SENSOR DASHBOARD =================
        st.markdown("## 📡 Live IoT Sensor Data")
        
        sensor = get_sensor_data()
        
        # Connection status indicator
        conn_status = "🟢 Online" if sensor["connection"] == "online" else "🔴 Offline"
        st.markdown(f'<div style="margin-bottom:15px;">ESP32 Status: <b>{conn_status}</b></div>', unsafe_allow_html=True)
        
        # Sensor cards with dynamic coloring
        c1, c2, c3, c4 = st.columns(4, gap="medium")
        
        with c1:
            moisture1 = sensor["soil_moisture"]
            card_class = get_sensor_card_class(moisture1, 30, 70)
            st.markdown(f'''
            <div class="glass sensor-card {card_class}">
                <h4>🌱 Part 1 Moisture</h4>
                <div class="metric-value">{moisture1:.1f}<span class="metric-unit">%</span></div>
                <div style="margin-top:10px; font-size:0.85rem;">
                    {"🚨 Critical - Water Now!" if moisture1 < 30 else "⚠️ Low" if moisture1 < 40 else "✅ Optimal" if moisture1 < 70 else "💧 Wet"}
                </div>
            </div>''', unsafe_allow_html=True)
        
        with c2:
            moisture2 = sensor["soil_moisture2"]
            card_class = get_sensor_card_class(moisture2, 30, 70)
            st.markdown(f'''
            <div class="glass sensor-card {card_class}">
                <h4>🌱 Part 2 Moisture</h4>
                <div class="metric-value">{moisture2:.1f}<span class="metric-unit">%</span></div>
                <div style="margin-top:10px; font-size:0.85rem;">
                    {"🚨 Critical - Water Now!" if moisture2 < 30 else "⚠️ Low" if moisture2 < 40 else "✅ Optimal" if moisture2 < 70 else "💧 Wet"}
                </div>
            </div>''', unsafe_allow_html=True)
        
        with c3:
            temp = sensor["soil_temp"]
            card_class = get_sensor_card_class(temp, 20, 35)
            st.markdown(f'''
            <div class="glass sensor-card {card_class}">
                <h4>🌡 Soil Temperature</h4>
                <div class="metric-value">{temp:.1f}<span class="metric-unit">°C</span></div>
                <div style="margin-top:10px; font-size:0.85rem;">
                    {"❄️ Cold" if temp < 15 else "⚠️ Cool" if temp < 20 else "✅ Optimal" if temp < 35 else "🔥 Hot"}
                </div>
            </div>''', unsafe_allow_html=True)
        
        with c4:
            hum = sensor["humidity"]
            pump = sensor["pump_status"]
            pump_class = "pump-active" if pump == "ON" else ""
            card_class = "sensor-optimal" if pump == "OFF" else "sensor-warning"
            st.markdown(f'''
            <div class="glass sensor-card {card_class}">
                <h4>🚿 Pump Status</h4>
                <div class="metric-value {pump_class}" style="font-size:2.5rem;">{pump}</div>
                <div style="margin-top:10px; font-size:0.85rem;">
                    💧 Ambient: {hum:.1f}%
                </div>
            </div>''', unsafe_allow_html=True)

        # ================= AUTOMATION LOGIC =================
        st.markdown("## ⚙️ Smart Automation")
        
        iot_status = iot_decision_logic(sensor, prediction)
        
        status_color = "#00ff96" if "optimal" in iot_status.lower() or "stable" in iot_status.lower() else \
                      "#ffc800" if "recommended" in iot_status.lower() or "light" in iot_status.lower() else "#ff3333"
        
        st.markdown(f'''
        <div class="glass" style="border-left: 4px solid {status_color};">
            <h4>🤖 AI Decision Engine</h4>
            <div style="font-size:1.3rem; color:{status_color}; margin:15px 0;">
                {iot_status}
            </div>
            <div style="font-size:0.9rem; opacity:0.8; margin-top:10px;">
                Based on: Soil Moisture ({sensor["soil_moisture"]:.1f}%, {sensor["soil_moisture2"]:.1f}%) + 
                Rain Prediction ({prediction:.1f}mm)
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # ================= FORECAST =================
        st.markdown("## 📊 Predictive Analytics")
        
        future_df = predict_next_days(model, df.tail(1))
        
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("### 🌧 5-Day Rainfall Forecast")
            st.line_chart(future_df.set_index("date"), height=300)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("### 📈 Trend Analysis")
            future_df["trend"] = future_df["rain"].diff()
            st.area_chart(future_df.set_index("date")[["trend"]], height=300)
            st.markdown('</div>', unsafe_allow_html=True)

        # ================= PANCHANG =================
        st.markdown("## 🪐 Panchang Astrological Data")
        
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        panchang_data = [
            ("🌙 Tithi", latest.get("tithi", "N/A")),
            ("⭐ Nakshatra", latest.get("nakshatra", "N/A")),
            ("📅 Vara", latest.get("vara", "N/A")),
            ("🌕 Moon Phase", latest.get("moon_phase", "N/A"))
        ]
        
        for col, (title, val) in zip([col1, col2, col3, col4], panchang_data):
            with col:
                st.markdown(f'''
                <div class="glass" style="text-align:center;">
                    <h4>{title}</h4>
                    <div style="font-size:1.2rem; color:#00c3ff; margin-top:10px;">{val}</div>
                </div>''', unsafe_allow_html=True)

        # ================= FOOTER =================
        st.markdown("""
        <div class="footer">
            <p>🌾 <b>MeghDristi</b> Smart Agriculture System</p>
            <p>AI-Powered Rainfall Prediction & IoT Irrigation</p>
            <p style="margin-top:10px; opacity:0.6;">Developed by Yogalakshmi & Ayush Jena | © 2026</p>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.info("Please check your ESP32 connection and try again.")

# Auto-refresh indicator at bottom
st.markdown("""
<div style="position:fixed; bottom:20px; right:20px; background:rgba(0,195,255,0.2); 
padding:10px 20px; border-radius:20px; font-size:0.8rem; color:#00c3ff; border:1px solid #00c3ff;">
    🔄 Auto-refresh: 5s
</div>
""", unsafe_allow_html=True)