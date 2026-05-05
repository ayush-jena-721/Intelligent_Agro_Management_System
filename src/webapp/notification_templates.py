"""
MeghDristi Notification Templates
One-time setup → Auto-fetch from Firestore → Send via FCM
"""

import os
import json
import time
import logging
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from string import Template

try:
    from firebase_admin import messaging
    from firebase_admin import firestore
    FCM_AVAILABLE = True
except ImportError:
    FCM_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class NotificationTemplate:
    """Reusable template with placeholders for dynamic data"""
    name: str
    title_template: str
    body_template: str
    category: str = "general"
    priority: str = "normal"
    sound: str = "default"
    data_fields: Dict[str, str] = field(default_factory=dict)
    condition_checker: Optional[Callable] = None  # Function to check if should send
    
    def render(self, context: Dict) -> Dict[str, str]:
        """Fill template with actual Firestore data"""
        title = Template(self.title_template).safe_substitute(context)
        body = Template(self.body_template).safe_substitute(context)
        
        # Build data payload
        data = {}
        for key, template_val in self.data_fields.items():
            data[key] = Template(template_val).safe_substitute(context)
        
        return {
            "title": title,
            "body": body,
            "data": data,
            "priority": self.priority,
            "sound": self.sound,
            "category": self.category
        }


# ═══════════════════════════════════════════════════════════════
# PRE-BUILT TEMPLATES (One-time setup, reuse forever)
# ═══════════════════════════════════════════════════════════════

TEMPLATES = {
    # IRRIGATION ALERTS
    "irrigation_on": NotificationTemplate(
        name="irrigation_on",
        title_template="🚨 IRRIGATION ACTIVATED",
        body_template="""Pump ON — Soil: ${soil_moisture1:.0f}%/${soil_moisture2:.0f}% | Temp: ${soil_temp:.0f}°C | AI: ${confidence:.0f}%
Reason: ${reason}
Tithi: ${tithi} | Nakshatra: ${nakshatra}""",
        category="irrigation",
        priority="high",
        sound="emergency",
        data_fields={
            "type": "irrigation",
            "action": "ON",
            "confidence": "${confidence}",
            "soil_1": "${soil_moisture1}",
            "soil_2": "${soil_moisture2}",
            "timestamp": "${timestamp}",
            "click_action": "open_irrigation"
        }
    ),
    
    "irrigation_medium": NotificationTemplate(
        name="irrigation_medium",
        title_template="💧 BUFFER IRRIGATION",
        body_template="""Pump MEDIUM — Soil: ${soil_moisture1:.0f}%/${soil_moisture2:.0f}%
${reason}
Rain forecast: ${rain_prediction:.1f}mm | AI: ${confidence:.0f}%""",
        category="irrigation",
        priority="normal",
        data_fields={
            "type": "irrigation",
            "action": "MEDIUM",
            "confidence": "${confidence}",
            "click_action": "open_irrigation"
        }
    ),
    
    "irrigation_off": NotificationTemplate(
        name="irrigation_off",
        title_template="✅ Irrigation Standby",
        body_template="""Pump OFF — Soil adequate: ${soil_moisture1:.0f}%/${soil_moisture2:.0f}%
${reason}
Rain: ${rain_prediction:.1f}mm | Temp: ${temperature:.0f}°C""",
        category="irrigation",
        priority="normal",
        data_fields={
            "type": "irrigation",
            "action": "OFF",
            "click_action": "open_irrigation"
        }
    ),
    
    # WEATHER ALERTS
    "weather_heavy_rain": NotificationTemplate(
        name="weather_heavy_rain",
        title_template="🌧️ Heavy Rain Alert",
        body_template="""${rain_prediction:.0f}mm heavy rain expected!
Tithi: ${tithi} | Nakshatra: ${nakshatra}
⚠️ STOP irrigation. Protect crops from waterlogging.""",
        category="weather",
        priority="high",
        sound="emergency",
        data_fields={
            "type": "weather",
            "prediction": "${rain_prediction}",
            "tithi": "${tithi}",
            "nakshatra": "${nakshatra}",
            "click_action": "open_weather"
        },
        condition_checker=lambda ctx: ctx.get("rain_prediction", 0) > 15
    ),
    
    "weather_moderate_rain": NotificationTemplate(
        name="weather_moderate_rain",
        title_template="🌦️ Moderate Rain Forecast",
        body_template="""${rain_prediction:.0f}mm rain expected in 24hrs
Tithi: ${tithi} | Temp: ${temperature:.0f}°C
💡 Delay irrigation 6-8 hours.""",
        category="weather",
        priority="normal",
        data_fields={
            "type": "weather",
            "prediction": "${rain_prediction}",
            "click_action": "open_weather"
        },
        condition_checker=lambda ctx: 5 < ctx.get("rain_prediction", 0) <= 15
    ),
    
    "weather_drought": NotificationTemplate(
        name="weather_drought",
        title_template="☀️ Drought Warning",
        body_template="""No rain + ${temperature:.0f}°C heat! Soil: ${soil_moisture1:.0f}%
🚨 URGENT: Check soil & irrigate immediately!
Nakshatra: ${nakshatra} (Agni-dominant)""",
        category="weather",
        priority="high",
        sound="emergency",
        data_fields={
            "type": "weather",
            "temperature": "${temperature}",
            "click_action": "open_weather"
        },
        condition_checker=lambda ctx: ctx.get("rain_prediction", 0) < 1 and ctx.get("temperature", 0) > 35
    ),
    
    # CRITICAL ALERTS
    "critical_soil_dry": NotificationTemplate(
        name="critical_soil_dry",
        title_template="🆘 CRITICAL: Soil Too Dry",
        body_template="""Soil moisture: ${soil_moisture1:.0f}%/${soil_moisture2:.0f}%!
Crop stress imminent. Pump auto-activated.
Check field NOW!""",
        category="critical",
        priority="high",
        sound="emergency",
        data_fields={
            "type": "critical",
            "alert_type": "soil_dry",
            "click_action": "open_dashboard"
        },
        condition_checker=lambda ctx: ctx.get("soil_moisture1", 100) < 20 or ctx.get("soil_moisture2", 100) < 20
    ),
    
    "critical_pump_failure": NotificationTemplate(
        name="critical_pump_failure",
        title_template="⚠️ Pump Failure Detected",
        body_template="""Pump not responding! Status: ${pump_status}
Soil: ${soil_moisture1:.0f}% | Temp: ${soil_temp:.0f}°C
Check power/connection immediately!""",
        category="critical",
        priority="high",
        sound="emergency",
        data_fields={
            "type": "critical",
            "alert_type": "pump_failure",
            "click_action": "open_dashboard"
        }
    ),
    
    "critical_device_offline": NotificationTemplate(
        name="critical_device_offline",
        title_template="📡 Device Offline",
        body_template="""ESP32 offline since ${last_seen}
Last soil: ${soil_moisture1:.0f}% | Temp: ${soil_temp:.0f}°C
Check WiFi/power supply!""",
        category="critical",
        priority="high",
        data_fields={
            "type": "critical",
            "alert_type": "connection_lost",
            "click_action": "open_dashboard"
        }
    ),
    
    # DAILY SUMMARY
    "daily_summary": NotificationTemplate(
        name="daily_summary",
        title_template="🌾 MeghDristi Daily Briefing",
        body_template="""Soil: ${soil_moisture1:.0f}%/${soil_moisture2:.0f}% | Temp: ${soil_temp:.0f}°C
Pump: ${pump_status} | Rain: ${rain_prediction:.0f}mm
Tithi: ${tithi} | Nakshatra: ${nakshatra}
Have a productive day! 🚜""",
        category="summary",
        priority="normal",
        data_fields={
            "type": "daily_summary",
            "click_action": "open_dashboard"
        }
    ),
    
    # TEST
    "test": NotificationTemplate(
        name="test",
        title_template="🌾 MeghDristi Test",
        body_template="""System check: Soil ${soil_moisture1:.0f}% | Temp ${soil_temp:.0f}°C
Notifications are working! You'll get real alerts here.""",
        category="test",
        priority="high",
        data_fields={
            "type": "test",
            "click_action": "open_settings"
        }
    )
}


# ═══════════════════════════════════════════════════════════════
# AUTO-FETCH & SEND ENGINE
# ═══════════════════════════════════════════════════════════════

class MeghDristiNotificationEngine:
    """
    Fetches live data from Firestore, picks template, sends notification
    """
    
    def __init__(self, db=None):
        self.db = db
        self.sent_log = {}  # Prevent duplicate sends
        
    def _get_db(self):
        if self.db is None:
            try:
                from webapp.firestore_client import get_firestore_client
                self.db = get_firestore_client()
            except:
                pass
        return self.db
    
    def _fetch_live_context(self) -> Dict:
        """
        Auto-fetch ALL data from Firestore in one go
        """
        context = {
            "timestamp": str(int(time.time())),
            "timestamp_iso": datetime.now().isoformat()
        }
        
        try:
            db = self._get_db()
            if db is None:
                return context
            
            # 1. Fetch latest sensor data
            sensor_doc = db.collection("sensor_readings").document("latest").get()
            if sensor_doc.exists:
                s = sensor_doc.to_dict()
                context.update({
                    "soil_moisture1": float(s.get("part1", s.get("soil_moisture", 0))),
                    "soil_moisture2": float(s.get("part2", s.get("soil_moisture2", 0))),
                    "soil_temp": float(s.get("temperature", s.get("soil_temp", 0))),
                    "humidity": float(s.get("humidity", 0)),
                    "temperature": float(s.get("ambient_temp", s.get("temperature", 0))),
                    "pump_status": s.get("pump_status", s.get("pump", "OFF")),
                    "last_seen": s.get("timestamp_iso", "unknown")
                })
            
            # 2. Fetch latest AI decision
            ai_doc = db.collection("sensor_readings").document("ai_decision").get()
            if ai_doc.exists:
                a = ai_doc.to_dict()
                context.update({
                    "pump_action": a.get("pump_action", "OFF"),
                    "confidence": float(a.get("confidence", 0)) * 100,
                    "reason": a.get("reason", "No decision yet"),
                    "details": a.get("details", "")
                })
            
            # 3. Fetch weather/panchang from latest reading
            # (Assuming you store these in Firestore too, or fetch from session)
            # Fallback to defaults if not in Firestore
            context.setdefault("rain_prediction", 0.0)
            context.setdefault("tithi", "Unknown")
            context.setdefault("nakshatra", "Unknown")
            context.setdefault("vara", "Unknown")
            
        except Exception as e:
            logger.error(f"Fetch context failed: {e}")
        
        return context
    
    def _should_send(self, template: NotificationTemplate, context: Dict) -> bool:
        """Check rate limiting and conditions"""
        # Rate limit: max 1 per template per 5 minutes
        key = f"{template.name}:{datetime.now().strftime('%H:%M')[:-1]}0"  # 10-min bucket
        if self.sent_log.get(key):
            return False
        
        # Check template condition
        if template.condition_checker and not template.condition_checker(context):
            return False
        
        return True
    
    def send(self, template_name: str, context: Optional[Dict] = None,
             topic: str = "all_farmers", force: bool = False) -> Dict:
        """
        Main send method: auto-fetch data, render template, send FCM
        """
        if not FCM_AVAILABLE:
            return {"status": "unavailable", "error": "FCM not initialized"}
        
        # Get template
        template = TEMPLATES.get(template_name)
        if not template:
            return {"status": "error", "error": f"Template '{template_name}' not found"}
        
        # Auto-fetch context if not provided
        if context is None:
            context = self._fetch_live_context()
        
        # Check conditions
        if not force and not self._should_send(template, context):
            return {"status": "skipped", "reason": "rate_limited or condition_not_met"}
        
        # Render template
        rendered = template.render(context)
        
        # Build FCM message
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=rendered["title"],
                    body=rendered["body"]
                ),
                data=rendered["data"],
                topic=topic,
                android=messaging.AndroidConfig(
                    priority="high" if rendered["priority"] == "high" else "normal",
                    notification=messaging.AndroidNotification(
                        sound=rendered["sound"],
                        channel_id=f"meghdristi_{template.category}",
                        priority="high" if rendered["priority"] == "high" else "default"
                    )
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            sound=rendered["sound"],
                            badge=1
                        )
                    )
                )
            )
            
            # SEND
            message_id = messaging.send(message)
            
            # Mark as sent
            key = f"{template.name}:{datetime.now().strftime('%H:%M')[:-1]}0"
            self.sent_log[key] = True
            
            result = {
                "status": "sent",
                "message_id": message_id,
                "template": template_name,
                "topic": topic,
                "title": rendered["title"],
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"📲 FCM sent: {template.name} | {rendered['title']}")
            return result
            
        except Exception as e:
            logger.error(f"FCM send failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def auto_send_all(self, context: Optional[Dict] = None) -> Dict[str, Dict]:
        """
        Check all templates and auto-send matching ones
        Run this every 15 minutes from Streamlit
        """
        if context is None:
            context = self._fetch_live_context()
        
        results = {}
        
        # Always check these
        priority_templates = [
            "critical_soil_dry",
            "critical_pump_failure", 
            "critical_device_offline",
            "weather_heavy_rain",
            "weather_drought"
        ]
        
        for name in priority_templates:
            results[name] = self.send(name, context)
        
        # Irrigation based on AI decision
        action = context.get("pump_action", "OFF")
        if action == "ON":
            results["irrigation"] = self.send("irrigation_on", context)
        elif action == "MEDIUM":
            results["irrigation"] = self.send("irrigation_medium", context)
        else:
            results["irrigation"] = self.send("irrigation_off", context)
        
        # Weather (moderate rain check)
        rain = context.get("rain_prediction", 0)
        if 5 < rain <= 15:
            results["weather"] = self.send("weather_moderate_rain", context)
        
        return results


# ═══════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

_engine = None

def get_engine() -> MeghDristiNotificationEngine:
    global _engine
    if _engine is None:
        _engine = MeghDristiNotificationEngine()
    return _engine

def notify(template_name: str, context: Optional[Dict] = None) -> Dict:
    """Send one notification by template name"""
    return get_engine().send(template_name, context)

def auto_notify() -> Dict[str, Dict]:
    """Auto-check all conditions and send relevant alerts"""
    return get_engine().auto_send_all()

def notify_test() -> Dict:
    """Send test notification"""
    return get_engine().send("test")

def notify_daily() -> Dict:
    """Send daily summary"""
    return get_engine().send("daily_summary")