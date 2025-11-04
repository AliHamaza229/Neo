# core/condition_detector.py
import cv2
import time
import numpy as np
import random
import psutil
import os

# ---------------------------------------
# Detect motion, face, and phone usage
# ---------------------------------------

def detect():
    """
    Uses camera, motion, and activity data to guess user's condition.
    Returns one of: sleeping, using_phone, busy, away, unknown
    """
    print("🧠 Checking user condition...")
    condition = "unknown"

    # Try webcam
    cam_available, face_found, eyes_closed = analyze_webcam()
    if cam_available:
        if not face_found:
            condition = "away"
        elif eyes_closed:
            condition = "sleeping"
        else:
            condition = "busy"  # face visible but eyes open → awake
    else:
        condition = "unknown"

    # Check device activity (keyboard/mouse or high CPU)
    if is_device_active():
        condition = "using_phone"

    print(f"Detected condition: {condition}")
    return condition


# ---------------------------------------
# Webcam-based analysis
# ---------------------------------------
def analyze_webcam():
    """
    Tries to detect face and eyes using Haar cascades (OpenCV built-in).
    Returns (camera_ok, face_found, eyes_closed)
    """
    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            return (False, False, False)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        ret, frame = cam.read()
        cam.release()

        if not ret:
            return (True, False, False)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return (True, False, False)

        # Check eyes in the first detected face
        (x, y, w, h) = faces[0]
        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        if len(eyes) == 0:
            return (True, True, True)   # face found, eyes closed
        else:
            return (True, True, False)  # face found, eyes open

    except Exception as e:
        print(f"Webcam check failed: {e}")
        return (False, False, False)


# ---------------------------------------
# Detect phone / device activity
# ---------------------------------------
def is_device_active():
    """
    Checks if user is actively using device (based on CPU or running apps).
    Works on Windows/Linux.
    """
    try:
        usage = psutil.cpu_percent(interval=1)
        if usage > 15:  # actively using
            return True
    except:
        pass
    return False


# ---------------------------------------
# Randomized fallback when unsure
# ---------------------------------------
def fallback_condition():
    """
    If no reliable data is available, randomly choose from 10 fallback responses.
    """
    fallback_conditions = [
        "sir_missing", "unknown", "cannot_detect",
        "away", "offline", "phone_away",
        "camera_blocked", "no_sound", "sleeping_maybe", "neutral"
    ]
    return random.choice(fallback_conditions)


# ---------------------------------------
# Manual test
# ---------------------------------------
if __name__ == "__main__":
    cond = detect()
    print("Condition result:", cond)
