# core/alert_manager.py

import time
import json
import os
from collections import defaultdict
from core import speech_io

# Path to saved call count data
ALERT_FILE = "data/alert_config.json"

# Numbers that Neo should alert about (like parents)
ALERT_CONTACTS = ["+1111111111", "+2222222222"]  # Replace later with your real contacts

# Threshold for alert (if someone calls more than this within a short time)
CALL_THRESHOLD = 3   # e.g., 3 calls
TIME_WINDOW = 180    # 3 minutes

# Memory of recent calls
recent_calls = defaultdict(list)

# ---------------------------------------
# Record incoming call attempt
# ---------------------------------------
def record_call(caller):
    """
    Records a new call attempt and checks for repeated calls.
    """
    num = caller["number"]
    t = time.time()
    recent_calls[num].append(t)
    # Keep only last few calls within time window
    recent_calls[num] = [x for x in recent_calls[num] if (t - x) < TIME_WINDOW]

    if len(recent_calls[num]) >= CALL_THRESHOLD:
        trigger_alert(caller)

# ---------------------------------------
# Trigger alert if repeated calls detected
# ---------------------------------------
def trigger_alert(caller):
    """
    Activates alert mode when a number calls too frequently.
    """
    print(f"⚠️ Alert: {caller['name']} is calling repeatedly!")
    speech_io.speak(f"Alert. {caller['name']} has been calling repeatedly.")
    save_alert(caller)

# ---------------------------------------
# Save alert info
# ---------------------------------------
def save_alert(caller):
    os.makedirs("data", exist_ok=True)
    data = {
        "caller": caller,
        "time": time.ctime(),
        "type": "repeated_call"
    }
    with open(ALERT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")
