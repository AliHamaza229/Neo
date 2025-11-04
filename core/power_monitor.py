# core/power_monitor.py

import psutil
import time
import json
import os
from core import speech_io

PARENT_NUMBERS = ["+1111111111", "+2222222222"]  # Replace with your actual contacts
BATTERY_LOW_THRESHOLD = 20   # percentage

# ---------------------------------------
# Check battery and send alert if low
# ---------------------------------------
def check_battery():
    """
    Checks battery level every few minutes. If low, sends an alert message.
    """
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return  # No battery sensor
        if battery.percent <= BATTERY_LOW_THRESHOLD and not battery.power_plugged:
            send_message("Device battery low. Please check on Neo's owner.")
    except Exception as e:
        print("Battery check error:", e)

# ---------------------------------------
# Simulate message sending (offline)
# ---------------------------------------
def send_message(msg):
    """
    In real app, this would send SMS via phone API. Here we log the message.
    """
    os.makedirs("data", exist_ok=True)
    log_path = "data/power_alerts.log"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(time.ctime() + " | " + msg + "\n")
    print(f"📩 Alert message saved: {msg}")
    speech_io.speak("Power alert recorded.")
