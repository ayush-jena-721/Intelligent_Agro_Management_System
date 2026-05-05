"""
Firebase Cloud Messaging (FCM) for MeghDristi
Sends FREE push notifications to farmer's phone via Firebase
Works with: Android, iOS, Web (PWA), no app store needed
"""

import os
import json
import time
import logging
from typing import List, Dict, Optional, Union, Any
from datetime import datetime
from dataclasses import dataclass

# Firebase Admin is already imported in your firestore setup
try:
    from firebase_admin import messaging
    from firebase_admin import firestore
    from firebase_admin import credentials
    FCM_AVAILABLE = True
except ImportError:
    FCM_AVAILABLE = False
    logging.warning("firebase-admin not available. FCM disabled.")

logger = logging.getLogger(__name__)

# Firestore collections
FCM_TOKENS_COLLECTION = "fcm_tokens"
NOTIFICATION_LOG_COLLECTION = "notification_logs"
AI_DECISION_DOC = "ai_decision"

@dataclass
class NotificationResult:
    """Structured result for notification sends"""
    status: str
    success_count: int = 0
    failure_count: int = 0
    total: int = 0
    message_ids: List[str] = None
    errors: List[str] = None
    provider: str = "fcm"
    timestamp: str = None
    
    def __post_init__(self):
        if self.message_ids is None:
            self.message_ids = []
        if self.errors is None:
            self.errors = []
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class MeghDristiFCM:
    """
    Firebase Cloud Messaging notification engine
    Integrates with existing Firebase Firestore project
    """
    
    def __init__(self, db=None):
        self.db = db
        self._last_notification = {}  # Rate limiting per topic/token
        self._daily_stats = {"sent": 0, "date": datetime.now().date()}
        
    def _get_db(self):
        """Lazy load Firestore from existing connection"""
        if self.db is None:
            try:
                # Import from your existing firestore module
                from webapp.firestore_client import get_firestore_client
                self.db = get_firestore_client()
            except Exception as e:
                logger.error(f"Failed to get Firestore: {e}")
        return self.db
    
    def _rate_limit(self, key: str, min_seconds: int = 60) -> bool:
        """Prevent notification spam"""
        now = time.time()
        last = self._last_notification.get(key, 0)
        if now - last < min_seconds:
            return False
        self._last_notification[key] = now
        return True
    
    def _log_notification(self, title: str, body: str, result: NotificationResult,
                          category: str, target: str):
        """Store notification history in Firestore"""
        try:
            db = self._get_db()
            if db:
                db.collection(NOTIFICATION_LOG_COLLECTION).add({
                    "title": title,
                    "body": body[:300],
                    "result": {
                        "status": result.status,
                        "success": result.success_count,
                        "failure": result.failure_count,
                        "total": result.total
                    },
                    "category": category,
                    "target": target,
                    "timestamp": firestore.SERVER_TIMESTAMP,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
        except Exception as e:
            logger.error(f"Notification log failed: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # TOKEN MANAGEMENT
    # ═══════════════════════════════════════════════════════════════
    
    def register_token(self, token: str, user_id: str = "default_farmer",
                       device_info: str = "unknown", platform: str = "web") -> bool:
        """
        Register a device for push notifications
        Call this from your mobile app / PWA when user allows notifications
        """
        try:
            db = self._get_db()
            if db is None:
                return False
            
            doc_ref = db.collection(FCM_TOKENS_COLLECTION).document(token)
            doc_ref.set({
                "token": token,
                "user_id": user_id,
                "device_info": device_info,
                "platform": platform,  # android, ios, web
                "active": True,
                "registered_at": firestore.SERVER_TIMESTAMP,
                "last_ping": firestore.SERVER_TIMESTAMP,
                "project": "megh-dristi"
            })
            
            logger.info(f"✅ FCM token registered: {token[:20]}...")
            return True
            
        except Exception as e:
            logger.error(f"Token registration failed: {e}")
            return False
    
    def get_active_tokens(self, user_id: Optional[str] = None) -> List[str]:
        """Get all active FCM tokens"""
        try:
            db = self._get_db()
            if db is None:
                return []
            
            query = db.collection(FCM_TOKENS_COLLECTION).where("active", "==", True)
            if user_id:
                query = query.where("user_id", "==", user_id)
            
            docs = query.stream()
            tokens = []
            for doc in docs:
                data = doc.to_dict()
                token = data.get("token")
                if token and len(token) > 20:
                    tokens.append(token)
            
            return tokens
            
        except Exception as e:
            logger.error(f"Failed to get tokens: {e}")
            return []
    
    def deactivate_token(self, token: str) -> bool:
        """Mark token inactive (e.g., app uninstalled)"""
        try:
            db = self._get_db()
            if db:
                db.collection(FCM_TOKENS_COLLECTION).document(token).update({
                    "active": False,
                    "deactivated_at": firestore.SERVER_TIMESTAMP
                })
            return True
        except Exception as e:
            logger.error(f"Deactivate failed: {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════════
    # CORE FCM SEND METHODS
    # ═══════════════════════════════════════════════════════════════
    
    def send_to_tokens(self, tokens: List[str], title: str, body: str,
                       data: Dict[str, str] = None, priority: str = "normal",
                       category: str = "general") -> NotificationResult:
        """
        Send push notification to specific device tokens
        """
        if not FCM_AVAILABLE:
            return NotificationResult(status="unavailable", errors=["FCM not initialized"])
        
        if not tokens:
            return NotificationResult(status="no_tokens", errors=["No FCM tokens registered"])
        
        # Deduplicate tokens
        unique_tokens = list(set(tokens))
        
        try:
            # Build Android-specific config
            android_config = messaging.AndroidConfig(
                priority="high" if priority == "high" else "normal",
                notification=messaging.AndroidNotification(
                    title=title,
                    body=body,
                    sound="default" if priority == "normal" else "emergency",
                    channel_id=f"meghdristi_{category}",
                    priority="high" if priority == "high" else "default",
                    icon="@mipmap/ic_launcher",
                    color="#00c3ff",
                    click_action="FLUTTER_NOTIFICATION_CLICK"
                ),
                ttl=3600  # 1 hour expiry
            )
            
            # Build iOS/APNS config
            apns_config = messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        alert=messaging.ApsAlert(title=title, body=body),
                        sound="default",
                        badge=1,
                        category=category
                    )
                ),
                headers={"apns-priority": "10" if priority == "high" else "5"}
            )
            
            # Build web/PWA config
            webpush_config = messaging.WebpushConfig(
                notification=messaging.WebpushNotification(
                    title=title,
                    body=body,
                    icon="/icon-192x192.png",
                    badge="/badge-72x72.png",
                    tag=category,
                    require_interaction=priority == "high"
                ),
                fcm_options=messaging.WebpushFCMOptions(
                    link="/dashboard"
                )
            )
            
            # Build the message
            message = messaging.MulticastMessage(
                notification=messaging.Notification(title=title, body=body),
                data=data or {},
                tokens=unique_tokens,
                android=android_config,
                apns=apns_config,
                webpush=webpush_config
            )
            
            # SEND via Firebase
            response = messaging.send_multicast(message)
            
            result = NotificationResult(
                status="sent",
                success_count=response.success_count,
                failure_count=response.failure_count,
                total=len(unique_tokens)
            )
            
            # Handle failures - deactivate invalid tokens
            for idx, resp in enumerate(response.responses):
                if resp.success:
                    result.message_ids.append(resp.message_id)
                else:
                    error_msg = str(resp.exception)
                    result.errors.append(error_msg)
                    
                    # Auto-deactivate invalid tokens
                    if any(err in error_msg.lower() for err in [
                        "registration-token-not-registered",
                        "invalid-registration-token",
                        "not-registered"
                    ]):
                        self.deactivate_token(unique_tokens[idx])
                        logger.info(f"Auto-deactivated invalid token: {unique_tokens[idx][:20]}...")
            
            self._log_notification(title, body, result, category, f"tokens:{len(unique_tokens)}")
            logger.info(f"📲 FCM sent: {result.success_count}/{result.total} delivered")
            return result
            
        except Exception as e:
            logger.error(f"FCM send failed: {e}")
            return NotificationResult(status="error", errors=[str(e)])
    
    def send_to_topic(self, topic: str, title: str, body: str,
                      data: Dict[str, str] = None, priority: str = "normal") -> NotificationResult:
        """
        Send to a topic (e.g., 'all_farmers', 'premium_users')
        Farmers subscribe to topics in their app/PWA
        """
        if not FCM_AVAILABLE:
            return NotificationResult(status="unavailable")
        
        try:
            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                data=data or {},
                topic=topic,
                android=messaging.AndroidConfig(
                    priority="high" if priority == "high" else "normal"
                )
            )
            
            message_id = messaging.send(message)
            
            result = NotificationResult(
                status="sent",
                success_count=1,
                message_ids=[message_id]
            )
            
            self._log_notification(title, body, result, "topic", f"topic:{topic}")
            return result
            
        except Exception as e:
            logger.error(f"Topic send failed: {e}")
            return NotificationResult(status="error", errors=[str(e)])
    
    # ═══════════════════════════════════════════════════════════════
    # AGRICULTURE-SPECIFIC NOTIFICATIONS
    # ═══════════════════════════════════════════════════════════════
    
    def notify_irrigation(self, pump_action: str, reason: str,
                          sensor_data: Dict, confidence: float = 0.0,
                          user_id: Optional[str] = None) -> NotificationResult:
        """
        Send irrigation decision to farmer's phone
        """
        if pump_action == "ON":
            title = "🚨 IRRIGATION ACTIVATED"
            body = f"Pump ON — Soil {sensor_data.get('soil_moisture',0):.0f}% critical. {reason[:50]}"
            priority = "high"
            sound = "emergency"
        elif pump_action == "MEDIUM":
            title = "💧 BUFFER IRRIGATION"
            body = f"Pump MEDIUM — {reason[:60]}"
            priority = "normal"
            sound = "notification"
        else:
            title = "✅ Irrigation Standby"
            body = f"Pump OFF — {reason[:60]}"
            priority = "normal"
            sound = "default"
        
        data = {
            "type": "irrigation",
            "action": pump_action,
            "confidence": str(confidence),
            "soil_1": str(sensor_data.get("soil_moisture", 0)),
            "soil_2": str(sensor_data.get("soil_moisture2", 0)),
            "temp": str(sensor_data.get("soil_temp", 0)),
            "timestamp": str(int(time.time())),
            "click_action": "open_irrigation"
        }
        
        tokens = self.get_active_tokens(user_id)
        return self.send_to_tokens(tokens, title, body, data, priority, "irrigation")
    
    def notify_weather(self, prediction: float, panchang_data: Dict,
                       weather_data: Dict, user_id: Optional[str] = None) -> NotificationResult:
        """
        Send weather alert to phone
        """
        if prediction > 15:
            title = "🌧️ Heavy Rain Alert"
            body = f"{prediction:.0f}mm rain coming! {panchang_data.get('tithi','')} tithi. Stop irrigation!"
            priority = "high"
        elif prediction > 5:
            title = "🌦️ Moderate Rain Forecast"
            body = f"{prediction:.0f}mm expected. Delay irrigation 6hrs."
            priority = "normal"
        elif prediction < 1 and weather_data.get("temperature", 28) > 35:
            title = "☀️ Drought Warning"
            body = f"No rain + {weather_data.get('temperature',28):.0f}°C heat! Check soil NOW."
            priority = "high"
        else:
            title = "🌤️ Weather Update"
            body = f"Rain: {prediction:.0f}mm | Temp: {weather_data.get('temperature',28):.0f}°C"
            priority = "normal"
        
        data = {
            "type": "weather",
            "prediction": str(prediction),
            "tithi": panchang_data.get("tithi", "Unknown"),
            "nakshatra": panchang_data.get("nakshatra", "Unknown"),
            "temperature": str(weather_data.get("temperature", 28)),
            "click_action": "open_weather"
        }
        
        tokens = self.get_active_tokens(user_id)
        return self.send_to_tokens(tokens, title, body, data, priority, "weather")
    
    def notify_critical(self, alert_type: str, sensor_data: Dict,
                        user_id: Optional[str] = None) -> NotificationResult:
        """
        Emergency critical alert
        """
        alerts = {
            "soil_dry": {
                "title": "🆘 CRITICAL: Soil Too Dry",
                "body": f"Moisture {sensor_data.get('soil_moisture',0):.0f}%! Crop dying! Irrigate NOW!"
            },
            "pump_failure": {
                "title": "⚠️ Pump Failure",
                "body": "Pump not responding! Check power/connection immediately!"
            },
            "connection_lost": {
                "title": "📡 Device Offline",
                "body": f"ESP32 offline since {sensor_data.get('timestamp','unknown')}. Check WiFi!"
            },
            "temp_extreme": {
                "title": "🔥 Extreme Heat Alert",
                "body": f"Soil temp {sensor_data.get('soil_temp',0):.0f}°C! Crop stress imminent!"
            }
        }
        
        alert = alerts.get(alert_type, {
            "title": "⚠️ Field Alert",
            "body": f"Sensor anomaly: {alert_type}"
        })
        
        data = {
            "type": "critical",
            "alert_type": alert_type,
            "soil_moisture": str(sensor_data.get("soil_moisture", 0)),
            "timestamp": str(int(time.time())),
            "click_action": "open_dashboard"
        }
        
        tokens = self.get_active_tokens(user_id)
        return self.send_to_tokens(tokens, alert["title"], alert["body"], 
                                   data, "high", "critical")
    
    def notify_daily_summary(self, sensor_data: Dict, prediction: float,
                             panchang_data: Dict = None,
                             user_id: Optional[str] = None) -> NotificationResult:
        """
        Scheduled daily briefing
        """
        title = "🌾 MeghDristi Daily Briefing"
        body = (
            f"Soil: {sensor_data.get('soil_moisture',0):.0f}%/{sensor_data.get('soil_moisture2',0):.0f}% | "
            f"Temp: {sensor_data.get('soil_temp',0):.0f}°C | "
            f"Pump: {sensor_data.get('pump_status','OFF')} | "
            f"Rain: {prediction:.0f}mm"
        )
        
        data = {
            "type": "daily_summary",
            "click_action": "open_dashboard"
        }
        
        tokens = self.get_active_tokens(user_id)
        return self.send_to_tokens(tokens, title, body, data, "normal", "summary")
    
    def notify_test(self, token: str) -> NotificationResult:
        """Send test notification to verify setup"""
        return self.send_to_tokens(
            [token],
            "🌾 MeghDristi Test",
            "Your notification system is working! You'll get alerts here.",
            {"type": "test", "click_action": "open_settings"},
            "high"
        )


# ═══════════════════════════════════════════════════════════════
# MODULE-LEVEL CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

_fcm_instance = None

def get_fcm() -> MeghDristiFCM:
    """Singleton FCM instance"""
    global _fcm_instance
    if _fcm_instance is None:
        _fcm_instance = MeghDristiFCM()
    return _fcm_instance

def fcm_irrigation(pump_action: str, reason: str, sensor_data: Dict,
                   confidence: float = 0.0, user_id: Optional[str] = None) -> NotificationResult:
    return get_fcm().notify_irrigation(pump_action, reason, sensor_data, confidence, user_id)

def fcm_weather(prediction: float, panchang_data: Dict, weather_data: Dict,
                user_id: Optional[str] = None) -> NotificationResult:
    return get_fcm().notify_weather(prediction, panchang_data, weather_data, user_id)

def fcm_critical(alert_type: str, sensor_data: Dict,
                 user_id: Optional[str] = None) -> NotificationResult:
    return get_fcm().notify_critical(alert_type, sensor_data, user_id)

def fcm_daily(sensor_data: Dict, prediction: float, panchang_data: Dict = None,
              user_id: Optional[str] = None) -> NotificationResult:
    return get_fcm().notify_daily_summary(sensor_data, prediction, panchang_data, user_id)

def register_fcm_token(token: str, user_id: str = "default_farmer",
                       device_info: str = "unknown") -> bool:
    return get_fcm().register_token(token, user_id, device_info)

def fcm_test(token: str) -> NotificationResult:
    return get_fcm().notify_test(token)