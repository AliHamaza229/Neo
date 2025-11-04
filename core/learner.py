# core/learner.py

import json
import os

USER_PROFILE = "data/user_profile.json"

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# ---------------- Profile functions ----------------
def load_profile():
    if not os.path.exists(USER_PROFILE):
        return {"habits": {}, "responses": {}}
    try:
        with open(USER_PROFILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        print("⚠️ Failed to parse profile. Using blank memory.")
        return {"habits": {}, "responses": {}}

def save_profile(profile):
    with open(USER_PROFILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4)

# ---------------- Learning functions ----------------
def learn_response(caller_id, situation, correct_reply):
    profile = load_profile()
    profile.setdefault("responses", {})
    profile["responses"].setdefault(caller_id, {})
    profile["responses"][caller_id][situation] = correct_reply
    save_profile(profile)
    print(f"💾 Learned response for {caller_id} under '{situation}': {correct_reply}")

def get_learned_response(caller_id, situation):
    profile = load_profile()
    return profile.get("responses", {}).get(caller_id, {}).get(situation)
