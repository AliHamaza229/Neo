# core/dialogue_manager.py

import os
import json
import random
import datetime
from core import speech_io, learner

# ----------------------------
# Predefined responses
# ----------------------------
PREDEFINED_RESPONSES = {
    "sleeping": [
        "Sir is sleeping right now. Can I take a message?",
        "Sir is resting. Please leave your message.",
        "Sir is currently asleep. Would you like to leave a message?",
    ],
    "away": [
        "Sir is away at the moment. Leave a message?",
        "Sir is not available currently. Can I record your message?",
        "Sir is out. Please tell me your message.",
        "Sir is busy. Do you want to leave a message?",
        "Sir is not here. I can take a message.",
        "Sir is currently occupied. Please leave a message.",
        "Sir is away for now. Can I record your message?",
        "Sir is not available. Would you like to leave a note?",
        "Sir is not around. I can take your message.",
        "Sir is away at the moment. Leave your message please.",
        # add more if needed up to 20
    ],
    "unknown": [
        "Hello! I will take a message for you.",
        "Hi! I can record your message for Sir.",
        "Hello! Please tell me your message.",
    ]
}

# ----------------------------
# Save caller message
# ----------------------------
def save_message(caller, message_text):
    os.makedirs("data/messages", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    caller_name = caller.get("name", "unknown")
    filename = f"data/messages/{caller_name}_{timestamp}.json"
    message = {
        "caller": caller,
        "message": message_text,
        "time": timestamp
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(message, f, indent=4)
    print(f"💾 Message saved: {filename}")

# ----------------------------
# Ask user feedback
# ----------------------------
def ask_user_feedback():
    print("🧠 Did Neo respond correctly? (type correct response or leave blank to skip)")
    feedback = input("Feedback: ").strip()
    return feedback if feedback else None

# ----------------------------
# Handle single incoming call
# ----------------------------
def handle_incoming_call(caller, user_condition):
    """
    Handles the entire interaction with one caller.
    """
    caller_id = caller.get("id", "unknown")

    # Speak user condition once
    condition_message = random.choice(PREDEFINED_RESPONSES.get(user_condition, PREDEFINED_RESPONSES["unknown"]))
    speech_io.speak(f"Detected that Sir is {user_condition}. {condition_message}")

    # Try learned response first
    learned_response = learner.get_learned_response(caller_id, user_condition)
    if learned_response:
        speech_io.speak(learned_response)

    # Ask caller for message
    speech_io.speak("Please tell your message. Say 'end', 'finished', or 'complete' to stop.")
    full_message = ""
    while True:
        line = speech_io.listen(duration=5)
        if not line:
            continue
        if any(word in line.lower() for word in ["end", "finished", "complete"]):
            break
        full_message += line + " "

    full_message = full_message.strip()
    save_message(caller, full_message)

    # Ask Sir for feedback
    user_feedback = ask_user_feedback()
    if user_feedback:
        learner.learn_response(caller_id, user_condition, user_feedback)
        speech_io.speak("🧠 Noted your feedback. I will remember this for next time.")

    speech_io.speak("✅ Message recorded successfully. Goodbye!")

# ----------------------------
# Example testing
# ----------------------------
if __name__ == "__main__":
    test_caller = {"id": "123", "name": "Mom", "phone": "+1111111111"}
    handle_incoming_call(test_caller, "away")
