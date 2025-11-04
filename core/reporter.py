import os, json
from core import speech_io, learner

MESSAGES_DIR = "data/messages"

def give_report():
    if not os.path.exists(MESSAGES_DIR):
        speech_io.speak("No messages yet, Sir.")
        return

    files = sorted(os.listdir(MESSAGES_DIR))
    if not files:
        speech_io.speak("No new messages to report, Sir.")
        return

    for file in files:
        with open(os.path.join(MESSAGES_DIR, file), "r", encoding="utf-8") as f:
            data = json.load(f)
        caller = data["caller"]["name"]
        msg = data["message"]
        report_phrase = learner.get_report_phrase(msg) or f"{caller} said: {msg}"
        speech_io.speak(report_phrase)
        print(f"🗒 {report_phrase}")

        correction = input("Sir, any correction? (type 'you have to say...' or Enter): ").strip()
        if correction.lower().startswith("you have to say"):
            new_phrase = correction.replace("you have to say", "").strip(": ")
            learner.learn_report_phrase(msg, new_phrase)
            print("✅ Learned new report phrasing.")
