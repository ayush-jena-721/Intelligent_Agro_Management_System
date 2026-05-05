"""
Firestore Client Module for MegDristi Weather Prototype
Handles all Firebase Firestore database operations
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

# Firebase imports
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIRESTORE_AVAILABLE = True
except ImportError:
    FIRESTORE_AVAILABLE = False
    firebase_admin = None
    credentials = None
    firestore = None


# ═══════════════════════════════════════════════════════════════
# FIRESTORE CONFIGURATION
# ═══════════════════════════════════════════════════════════════
FIREBASE_PROJECT_ID = "megh-dristi"
FIRESTORE_COLLECTION = "sensor_readings"
FIRESTORE_LATEST_DOC = "latest"
FIRESTORE_AI_DECISION_DOC = "ai_decision"
FIRESTORE_HISTORY_COLLECTION = "history"
FIRESTORE_COMMANDS_COLLECTION = "commands"

# Global Firestore database client (singleton pattern)
_firestore_db: Optional[Any] = None


# ═══════════════════════════════════════════════════════════════
# INITIALIZATION & CLIENT MANAGEMENT
# ═══════════════════════════════════════════════════════════════
def get_firestore_client() -> Optional[Any]:
    """
    Initialize and return Firestore client (singleton pattern)
    
    Returns:
        Firestore client instance or None if initialization fails
    """
    global _firestore_db
    
    if not FIRESTORE_AVAILABLE:
        print("⚠️ firebase-admin not installed. Run: pip install firebase-admin")
        return None
    
    if _firestore_db is not None:
        return _firestore_db
    
    try:
        if not firebase_admin._apps:
            # Determine the base directory for service account file
            base_dir = Path(__file__).resolve().parents[2]
            
            # Try multiple credential sources
            env_cred = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
            candidate_paths = [
                Path(env_cred) if env_cred else None,
                base_dir / 'config' / 'megh-dristi-firebase-service-account.json',
                base_dir / 'src' / 'config' / 'megh-dristi-firebase-service-account.json',
            ]
            
            # Find the first existing credential file
            cred_path = next((p for p in candidate_paths if p is not None and p.exists()), None)
            
            if cred_path is not None:
                # Initialize with service account credentials
                cred = credentials.Certificate(str(cred_path))
                firebase_admin.initialize_app(cred, {'projectId': FIREBASE_PROJECT_ID})
                print(f"🔥 Firestore initialized with service account: {cred_path}")
            else:
                try:
                    # Try application default credentials (for GCP/cloud environments)
                    firebase_admin.initialize_app(
                        credentials.ApplicationDefault(),
                        {'projectId': FIREBASE_PROJECT_ID}
                    )
                    print("🔥 Firestore initialized with application default credentials")
                except Exception:
                    # Initialize without credentials (for emulator or public data)
                    firebase_admin.initialize_app(
                        options={'projectId': FIREBASE_PROJECT_ID}
                    )
                    print("🔥 Firestore initialized without credentials (emulator/public)")
        
        _firestore_db = firestore.client()
        return _firestore_db
    
    except Exception as e:
        print(f"❌ Firestore initialization failed: {e}")
        return None


def reset_firestore_client():
    """Reset the Firestore client (useful for testing)"""
    global _firestore_db
    _firestore_db = None
    if FIRESTORE_AVAILABLE and firebase_admin._apps:
        firebase_admin.delete_app(firebase_admin.get_app())


# ═══════════════════════════════════════════════════════════════
# SENSOR DATA OPERATIONS
# ═══════════════════════════════════════════════════════════════
def get_sensor_data_firestore() -> Dict[str, Any]:
    """
    Fetch real-time sensor data from Firestore
    
    Returns:
        Dictionary with sensor readings or simulated data on failure
    """
    try:
        db = get_firestore_client()
        if db is None:
            raise Exception("Firestore client not available")
        
        # Get latest document from sensor_readings collection
        doc_ref = db.collection(FIRESTORE_COLLECTION).document(FIRESTORE_LATEST_DOC)
        doc = doc_ref.get()
        
        if not doc.exists:
            # Fallback: try to get the most recent document from history
            history_ref = db.collection(FIRESTORE_COLLECTION).document("history_data").collection("readings")
            docs = history_ref.order_by("timestamp_epoch", direction=firestore.Query.DESCENDING).limit(1).stream()
            
            latest_doc = None
            for d in docs:
                latest_doc = d
                break
            
            if latest_doc is None:
                raise Exception("No sensor data found in Firestore")
            
            data = latest_doc.to_dict()
        else:
            data = doc.to_dict()
        
        # Parse Firestore data structure (matches ESP32 format)
        sensor_data = {
            "soil_moisture": float(data.get("part1", data.get("soil_moisture", data.get("moisture1", 0)))),
            "soil_moisture2": float(data.get("part2", data.get("soil_moisture2", data.get("moisture2", 0)))),
            "soil_temp": float(data.get("temperature", data.get("soil_temp", data.get("temp", 0)))),
            "humidity": float(data.get("humidity", 0)),
            "temperature": float(data.get("ambient_temp", data.get("temperature", 0))),
            "pump_status": data.get("pump_status", data.get("pump", "OFF")),
            "connection": "online",
            "timestamp": data.get("timestamp_iso", data.get("timestamp", datetime.now().isoformat())),
            "timestamp_epoch": data.get("timestamp_epoch", int(time.time())),
            "source": "firestore",
            "raw_data": data
        }
        
        # Auto pump logic: only turn pump OFF when both sensor readings are at safe levels
        if sensor_data["soil_moisture"] >= 85 and sensor_data["soil_moisture2"] >= 75:
            sensor_data["pump_status"] = "OFF"
        else:
            sensor_data["pump_status"] = "ON"
        
        return sensor_data
    
    except Exception as e:
        # Fallback to simulated data
        import random
        return {
            "soil_moisture": random.uniform(25, 45),
            "soil_moisture2": random.uniform(30, 50),
            "soil_temp": random.uniform(26, 32),
            "humidity": random.uniform(55, 75),
            "temperature": random.uniform(28, 35),
            "pump_status": "OFF",
            "connection": "simulated",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp_epoch": int(time.time()),
            "source": "simulated",
            "error": str(e)
        }


def get_sensor_history_firestore(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetch sensor reading history from Firestore
    
    Args:
        limit: Maximum number of records to retrieve
    
    Returns:
        List of historical sensor data dictionaries
    """
    try:
        db = get_firestore_client()
        if db is None:
            return []
        
        history_ref = db.collection(FIRESTORE_COLLECTION).document("history_data").collection("readings")
        docs = history_ref.order_by("timestamp_epoch", direction=firestore.Query.DESCENDING).limit(limit).stream()
        
        history_list = []
        for doc in docs:
            data = doc.to_dict()
            data['firestore_id'] = doc.id
            history_list.append(data)
        
        return history_list
    
    except Exception as e:
        print(f"Error fetching sensor history: {e}")
        return []


def write_sensor_data_firestore(sensor_data: Dict[str, Any]) -> bool:
    """
    Write sensor data to Firestore
    
    Args:
        sensor_data: Dictionary containing sensor readings
    
    Returns:
        True if successful, False otherwise
    """
    try:
        db = get_firestore_client()
        if db is None:
            return False
        
        # Write to latest document
        latest_ref = db.collection(FIRESTORE_COLLECTION).document(FIRESTORE_LATEST_DOC)
        latest_ref.set(sensor_data)
        
        # Also append to history
        history_ref = db.collection(FIRESTORE_COLLECTION).document("history_data").collection("readings")
        history_ref.add(sensor_data)
        
        return True
    
    except Exception as e:
        print(f"Error writing sensor data: {e}")
        return False


# ═══════════════════════════════════════════════════════════════
# AI DECISION OPERATIONS
# ═══════════════════════════════════════════════════════════════
def write_ai_decision_firestore(
    pump_action: str,
    reason: str,
    details: Dict[str, Any],
    confidence: float = 0.0
) -> bool:
    """
    Write AI irrigation decision to Firestore
    
    Args:
        pump_action: Action taken (ON/OFF)
        reason: Reason for the decision
        details: Additional details about the decision
        confidence: Confidence score (0.0-1.0)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        db = get_firestore_client()
        if db is None:
            return False
        
        decision_ref = db.collection(FIRESTORE_COLLECTION).document(FIRESTORE_AI_DECISION_DOC)
        decision_ref.set({
            "pump_action": pump_action,
            "reason": reason,
            "details": details,
            "confidence": confidence,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "source": "ai_engine",
            "decision_id": f"ai_{int(time.time())}"
        })
        return True
    
    except Exception as e:
        print(f"Failed to write AI decision: {e}")
        return False


def get_ai_decision_firestore() -> Optional[Dict[str, Any]]:
    """
    Retrieve the latest AI irrigation decision from Firestore
    
    Returns:
        Dictionary containing AI decision or None if not found
    """
    try:
        db = get_firestore_client()
        if db is None:
            return None
        
        doc_ref = db.collection(FIRESTORE_COLLECTION).document(FIRESTORE_AI_DECISION_DOC)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        
        return None
    
    except Exception as e:
        print(f"Error retrieving AI decision: {e}")
        return None


def get_ai_decision_history_firestore(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Fetch AI decision history from Firestore
    
    Args:
        limit: Maximum number of decisions to retrieve
    
    Returns:
        List of historical AI decisions
    """
    try:
        db = get_firestore_client()
        if db is None:
            return []
        
        decisions_ref = db.collection(FIRESTORE_COLLECTION).document("ai_history").collection("decisions")
        docs = decisions_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit).stream()
        
        decision_list = []
        for doc in docs:
            data = doc.to_dict()
            data['firestore_id'] = doc.id
            decision_list.append(data)
        
        return decision_list
    
    except Exception as e:
        print(f"Error fetching AI decision history: {e}")
        return []


# ═══════════════════════════════════════════════════════════════
# PUMP COMMAND OPERATIONS
# ═══════════════════════════════════════════════════════════════
def write_pump_command_firestore(
    command: str,
    reason: str = "Manual",
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Write pump command to Firestore
    
    Args:
        command: Command (ON/OFF)
        reason: Reason for the command
        metadata: Additional metadata
    
    Returns:
        True if successful, False otherwise
    """
    try:
        db = get_firestore_client()
        if db is None:
            return False
        
        commands_ref = db.collection(FIRESTORE_COMMANDS_COLLECTION)
        commands_ref.add({
            "command": command,
            "reason": reason,
            "metadata": metadata or {},
            "timestamp": firestore.SERVER_TIMESTAMP,
            "command_id": f"cmd_{int(time.time())}"
        })
        return True
    
    except Exception as e:
        print(f"Error writing pump command: {e}")
        return False


def get_pending_pump_commands_firestore() -> List[Dict[str, Any]]:
    """
    Retrieve pending pump commands from Firestore
    
    Returns:
        List of pending pump commands
    """
    try:
        db = get_firestore_client()
        if db is None:
            return []
        
        commands_ref = db.collection(FIRESTORE_COMMANDS_COLLECTION)
        docs = commands_ref.where("status", "==", "pending").order_by("timestamp").stream()
        
        command_list = []
        for doc in docs:
            data = doc.to_dict()
            data['firestore_id'] = doc.id
            command_list.append(data)
        
        return command_list
    
    except Exception as e:
        print(f"Error retrieving pump commands: {e}")
        return []


def mark_command_executed_firestore(command_id: str) -> bool:
    """
    Mark a pump command as executed
    
    Args:
        command_id: Firestore document ID of the command
    
    Returns:
        True if successful, False otherwise
    """
    try:
        db = get_firestore_client()
        if db is None:
            return False
        
        db.collection(FIRESTORE_COMMANDS_COLLECTION).document(command_id).update({
            "status": "executed",
            "executed_at": firestore.SERVER_TIMESTAMP
        })
        return True
    
    except Exception as e:
        print(f"Error updating command status: {e}")
        return False


# ═══════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def is_firestore_available() -> bool:
    """Check if Firestore is available"""
    return FIRESTORE_AVAILABLE


def get_firestore_status() -> Dict[str, Any]:
    """Get Firestore connection status"""
    try:
        db = get_firestore_client()
        if db is None:
            return {"status": "unavailable", "reason": "Client not initialized"}
        
        # Try a simple read to verify connection
        _ = db.collection(FIRESTORE_COLLECTION).document(FIRESTORE_LATEST_DOC).get()
        return {"status": "connected", "timestamp": datetime.now().isoformat()}
    
    except Exception as e:
        return {"status": "error", "reason": str(e)}


if __name__ == "__main__":
    # Test the module
    print("Firestore Client Module")
    print(f"Available: {is_firestore_available()}")
    print(f"Status: {get_firestore_status()}")
