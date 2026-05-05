import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import requests
from pydantic import BaseModel
import time
import json

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
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()
    st.session_state.sensor_data = None
    st.session_state.connection_status = "unknown"

# Auto-refresh every 3 seconds
st.markdown("""
<script>
    setTimeout(function(){
        window.location.reload();
    }, 3000);
</script>
""", unsafe_allow_html=True)

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');

* { font-family: 'Rajdhani', sans-serif; }

.block-container { padding: 1rem 2rem; max-width: 100%; }

.main {
    background: linear-gradient(135deg, #0a1628 0%, #1a2a4a 50%, #0f2847 100%);
    color: #ffffff;
}

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

.metric-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(180deg, #ffffff 0%, #00c3ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}

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

.debug-box {
    background: rgba(255, 50, 50, 0.1);
    border: 1px solid #ff3333;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    font-family: monospace;
    font-size: 0.85rem;
    color: #ff9999;
}

.success-box {
    background: rgba(0, 255, 150, 0.1);
    border: 1px solid #00ff96;
    color: #00ff96;
}

.timestamp {
    text-align: right;
    color: #88ccff;
    font-size: 0.8rem;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="connection-bar"></div>', unsafe_allow_html=True)

st.markdown("""
<h1>🌾 MeghDristi</h1>
<p style='text-align:center; color:#88ccff; font-size:1.1rem; margin-bottom:30px;'>
    AI-Powered Rainfall Prediction & Smart IoT Irrigation System
</p>
""", unsafe_allow_html=True)

current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f'<div class="timestamp">🔄 Last Updated: {current_time} | Auto-refresh: 3s</div>', unsafe_allow_html=True)

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
    
    # ESP32 Configuration
    st.header("🔗 ESP32 Configuration")
    ESP32_IP = st.text_input("ESP32 IP Address", value="10.213.32.75")
    ESP32_URL = f"http://{ESP32_IP}/"
    st.caption(f"URL: {ESP32_URL}")

# ---------------- MODEL & DATA ----------------
@st.cache_resource
def get_model():
    return load_model()

model = get_model()

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

# ---------------- IOT SENSOR FETCHER - FIXED ----------------
@st.cache_data(ttl=2)  # Cache for 2 seconds only
def get_sensor_data(esp32_url):
    """
    Fetch sensor data from ESP32 with detailed error handling
    """
    debug_info = {
        "url": esp32_url,
        "timestamp": pd.Timestamp.now().isoformat(),
        "steps": []
    }
    
    try:
        # Step 1: Attempt connection
        debug_info["steps"].append("Attempting HTTP GET...")
        
        # Disable SSL warnings and set headers
        headers = {
            'User-Agent': 'MeghDristi-Client/1.0',
            'Accept': 'application/json'
        }
        
        res = requests.get(
            esp32_url, 
            timeout=5,  # Increased timeout
            headers=headers,
            verify=False  # Skip SSL verification if needed
        )
        
        debug_info["steps"].append(f"Response received: Status {res.status_code}")
        debug_info["status_code"] = res.status_code
        
        if res.status_code == 200:
            # Step 2: Parse JSON
            try:
                data = res.json()
                debug_info["steps"].append(f"JSON parsed successfully: {json.dumps(data)[:100]}...")
                debug_info["raw_data"] = data
                
                # Determine pump status
                pump_status = "OFF"
                plant1 = data.get("plant1", data.get("soil_moisture", 100))
                plant2 = data.get("plant2", data.get("soil_moisture2", 100))
                
                if plant1 < 30 or plant2 < 30:
                    pump_status = "ON"
                
                result = {
                    "soil_moisture": plant1,
                    "soil_moisture2": plant2,
                    "soil_temp": data.get("temperature", data.get("soil_temp", 0)),
                    "humidity": data.get("humidity", 0),
                    "pump_status": pump_status,
                    "connection": "online",
                    "raw_data": data,
                    "debug_info": debug_info
                }
                
                debug_info["steps"].append(f"Success: {result['soil_moisture']:.1f}%, {result['soil_moisture2']:.1f}%")
                return result
                
            except json.JSONDecodeError as e:
                debug_info["steps"].append(f"JSON parse error: {str(e)}")
                debug_info["response_text"] = res.text[:200]
                raise Exception(f"Invalid JSON: {res.text[:100]}")
        else:
            raise Exception(f"HTTP {res.status_code}: {res.reason}")
            
    except requests.exceptions.ConnectTimeout:
        debug_info["steps"].append("ERROR: Connection timeout")
        return {
            "soil_moisture": 0, "soil_moisture2": 0, "soil_temp": 0,
            "humidity": 0, "pump_status": "TIMEOUT",
            "connection": "offline",
            "error": "Connection timeout - ESP32 not responding",
            "debug_info": debug_info
        }
        
    except requests.exceptions.ConnectionError as e:
        debug_info["steps"].append(f"ERROR: Connection refused - {str(e)}")
        return {
            "soil_moisture": 0, "soil_moisture2": 0, "soil_temp": 0,
            "humidity": 0, "pump_status": "CONN_ERR",
            "connection": "offline",
            "error": f"Cannot connect to ESP32 at {esp32_url}",
            "debug_info": debug_info
        }
        
    except Exception as e:
        debug_info["steps"].append(f"ERROR: {str(e)}")
        return {
            "soil_moisture": 0, "soil_moisture2": 0, "soil_temp": 0,
            "humidity": 0, "pump_status": "ERROR",
            "connection": "offline",
            "error": str(e),
            "debug_info": debug_info
        }

def get_sensor_card_class(value, optimal_min=40, optimal_max=70):
    if value < optimal_min:
        return "sensor-critical"
    elif value > optimal_max:
        return "sensor-warning"
    return "sensor-optimal"

def iot_decision_logic(sensor, prediction):
    if sensor["connection"] == "offline":
        return "⚠️ Sensor Offline - Manual Mode"
    
    plant1 = sensor["soil_moisture"]
    plant2 = sensor["soil_moisture2"]
    avg_moisture = (plant1 + plant2) / 2
    
    if plant1 < 20 or plant2 < 20:
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

# ================= DEBUG SECTION =================
st.markdown("## 🔧 Connection Debugger")

ESP32_URL = f"http://{ESP32_IP}/"

# Test connection immediately
with st.spinner("Testing ESP32 connection..."):
    sensor = get_sensor_data(ESP32_URL)

# Show debug info
if sensor.get("debug_info"):
    debug = sensor["debug_info"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**URL:** `{debug['url']}`")
        st.markdown(f"**Time:** `{debug['timestamp']}`")
        st.markdown(f"**Status:** `{sensor['connection'].upper()}`")
        
        if sensor.get("error"):
            st.markdown(f"**Error:** `{sensor['error']}`")
    
    with col2:
        st.markdown("**Connection Steps:**")
        for step in debug.get("steps", []):
            icon = "✅" if "Success" in step or "parsed" in step else "⏳" if "Attempting" in step else "❌"
            st.markdown(f"{icon} {step}")
    
    # Show raw data if available
    if "raw_data" in debug:
        st.markdown("**Raw ESP32 Response:**")
        st.code(json.dumps(debug["raw_data"], indent=2), language="json")

# Connection status indicator
conn_color = "#00ff96" if sensor["connection"] == "online" else "#ff3333"
st.markdown(f"""
<div style="padding:15px; border-radius:10px; background:rgba(0,0,0,0.3); border:2px solid {conn_color}; margin:20px 0;">
    <h3 style="color:{conn_color}; margin:0;">
        {"🟢 ESP32 CONNECTED" if sensor["connection"] == "online" else "🔴 ESP32 OFFLINE"}
    </h3>
    <p style="margin:5px 0 0 0; opacity:0.8;">
        {f"Plant1: {sensor['soil_moisture']:.1f}% | Plant2: {sensor['soil_moisture2']:.1f}%" if sensor["connection"] == "online" else sensor.get("error", "Check IP address and network")}
    </p>
</div>
""", unsafe_allow_html=True)

# ================= MAIN DASHBOARD =================
if st.button("🌧️ Predict Rainfall & Load IoT Data", use_container_width=True):
    try:
        # Re-fetch sensor data on button press
        sensor = get_sensor_data(ESP32_URL)
        
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
                <h4>🌧 Rainfall</h4>
                <div class="metric-value">{prediction:.1f}<span style="font-size:1rem;">mm</span></div>
                <div style="margin-top:10px; color:{"#ff3333" if prediction > 10 else "#00ff96"};">
                    {"Heavy Rain" if prediction > 10 else "Light Rain" if prediction > 0 else "No Rain"}
                </div>
            </div>''', unsafe_allow_html=True)
        
        with col2:
            temp_val = latest.get("temperature_2m", 0)
            st.markdown(f'''
            <div class="glass">
                <h4>🌡 Temperature</h4>
                <div class="metric-value">{temp_val:.1f}<span style="font-size:1rem;">°C</span></div>
                <div style="margin-top:10px; color:{"#ff3333" if temp_val > 35 else "#00ff96"};">
                    {"Hot" if temp_val > 35 else "Cold" if temp_val < 15 else "Optimal"}
                </div>
            </div>''', unsafe_allow_html=True)
        
        with col3:
            hum_val = latest.get("humidity", 0)
            st.markdown(f'''
            <div class="glass">
                <h4>💧 Humidity</h4>
                <div class="metric-value">{hum_val:.1f}<span style="font-size:1rem;">%</span></div>
                <div style="margin-top:10px; color:{"#ffc800" if hum_val < 30 else "#00ff96"};">
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
        
        if sensor["connection"] == "online":
            c1, c2, c3, c4 = st.columns(4, gap="medium")
            
            with c1:
                moisture1 = sensor["soil_moisture"]
                card_class = get_sensor_card_class(moisture1, 30, 70)
                status_text = "🚨 Critical" if moisture1 < 30 else "⚠️ Low" if moisture1 < 40 else "✅ Optimal" if moisture1 < 70 else "💧 Wet"
                st.markdown(f'''
                <div class="glass sensor-card {card_class}">
                    <h4>🌱 Plant 1 Moisture</h4>
                    <div class="metric-value">{moisture1:.1f}<span style="font-size:1rem;">%</span></div>
                    <div style="margin-top:10px; font-size:0.9rem;">{status_text}</div>
                </div>''', unsafe_allow_html=True)
            
            with c2:
                moisture2 = sensor["soil_moisture2"]
                card_class = get_sensor_card_class(moisture2, 30, 70)
                status_text = "🚨 Critical" if moisture2 < 30 else "⚠️ Low" if moisture2 < 40 else "✅ Optimal" if moisture2 < 70 else "💧 Wet"
                st.markdown(f'''
                <div class="glass sensor-card {card_class}">
                    <h4>🌱 Plant 2 Moisture</h4>
                    <div class="metric-value">{moisture2:.1f}<span style="font-size:1rem;">%</span></div>
                    <div style="margin-top:10px; font-size:0.9rem;">{status_text}</div>
                </div>''', unsafe_allow_html=True)
            
            with c3:
                temp = sensor["soil_temp"]
                card_class = get_sensor_card_class(temp, 20, 35)
                status_text = "❄️ Cold" if temp < 15 else "⚠️ Cool" if temp < 20 else "✅ Optimal" if temp < 35 else "🔥 Hot"
                st.markdown(f'''
                <div class="glass sensor-card {card_class}">
                    <h4>🌡 Soil Temperature</h4>
                    <div class="metric-value">{temp:.1f}<span style="font-size:1rem;">°C</span></div>
                    <div style="margin-top:10px; font-size:0.9rem;">{status_text}</div>
                </div>''', unsafe_allow_html=True)
            
            with c4:
                hum = sensor["humidity"]
                pump = sensor["pump_status"]
                card_class = "sensor-optimal" if pump == "OFF" else "sensor-warning"
                st.markdown(f'''
                <div class="glass sensor-card {card_class}">
                    <h4>🚿 Pump Status</h4>
                    <div style="font-size:2.5rem; font-weight:bold; color:{"#00ff96" if pump == "OFF" else "#ffc800"};">{pump}</div>
                    <div style="margin-top:10px; font-size:0.9rem;">💧 Ambient: {hum:.1f}%</div>
                </div>''', unsafe_allow_html=True)

            # ================= AUTOMATION LOGIC =================
            st.markdown("## ⚙️ Smart Automation")
            
            iot_status = iot_decision_logic(sensor, prediction)
            status_color = "#00ff96" if "optimal" in iot_status.lower() or "stable" in iot_status.lower() else \
                          "#ffc800" if "recommended" in iot_status.lower() else "#ff3333"
            
            st.markdown(f'''
            <div class="glass" style="border-left: 4px solid {status_color};">
                <h4>🤖 AI Decision Engine</h4>
                <div style="font-size:1.3rem; color:{status_color}; margin:15px 0;">
                    {iot_status}
                </div>
                <div style="font-size:0.9rem; opacity:0.8;">
                    Based on: Soil Moisture ({sensor["soil_moisture"]:.1f}%, {sensor["soil_moisture2"]:.1f}%) + 
                    Rain Prediction ({prediction:.1f}mm)
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
        else:
            st.error("❌ ESP32 Offline - Cannot display sensor data")
            st.info(f"**Error:** {sensor.get('error', 'Unknown error')}")
            st.markdown("**Troubleshooting:**")
            st.markdown("1. Check ESP32 is powered ON")
            st.markdown("2. Verify IP address `10.213.32.75` is correct")
            st.markdown("3. Ensure PC and ESP32 are on same WiFi network")
            st.markdown("4. Test in browser: `http://10.213.32.75/`")

        # ================= FORECAST =================
        st.markdown("## 📊 Predictive Analytics")
        
        future_df = predict_next_days(model, df.tail(1))
        
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            st.markdown('<div style="background:rgba(16,30,60,0.4); border-radius:15px; padding:20px;">', unsafe_allow_html=True)
            st.markdown("### 🌧 5-Day Rainfall Forecast")
            st.line_chart(future_df.set_index("date"), height=300)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div style="background:rgba(16,30,60,0.4); border-radius:15px; padding:20px;">', unsafe_allow_html=True)
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
        <div style="text-align:center; padding:30px; margin-top:40px; border-top:1px solid rgba(0,195,255,0.2); color:#88ccff;">
            <p>🌾 <b>MeghDristi</b> Smart Agriculture System</p>
            <p>AI-Powered Rainfall Prediction & IoT Irrigation</p>
            <p style="margin-top:10px; opacity:0.6;">Developed by Yogalakshmi & Ayush Jena | © 2026</p>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Dashboard Error: {e}")
        import traceback
        st.code(traceback.format_exc())

# Auto-refresh indicator
st.markdown("""
<div style="position:fixed; bottom:20px; right:20px; background:rgba(0,195,255,0.2); 
padding:10px 20px; border-radius:20px; font-size:0.8rem; color:#00c3ff; border:1px solid #00c3ff;">
    🔄 Auto-refresh: 3s | ESP32: {}
</div>
""".format("ONLINE ✅" if sensor["connection"] == "online" else "OFFLINE ❌"), unsafe_allow_html=True)