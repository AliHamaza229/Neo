# core/call_simulator.py
import time
import random
import threading

# -------------------------------------------------
# Fake call states
# -------------------------------------------------
CALLERS = [
    {"name": "Mom", "number": "+1111111111"},
    {"name": "Dad", "number": "+2222222222"},
    {"name": "Best Friend", "number": "+3333333333"},
    {"name": "Boss", "number": "+4444444444"},
    {"name": "Unknown", "number": "+5555555555"}
]

current_call = None
user_picked = False
incoming = False
call_thread = None

# -------------------------------------------------
# Simulate incoming call every random seconds
# -------------------------------------------------
def simulate_incoming_calls():
    """
    Randomly triggers incoming calls every 15–60 seconds.
    This runs in the background and updates the global state.
    """
    global incoming, current_call, call_thread
    def _simulate():
        global incoming, current_call, user_picked
        while True:
            wait_time = random.randint(15, 60)
            time.sleep(wait_time)
            current_call = random.choice(CALLERS)
            incoming = True
            user_picked = False
            print(f"\n📞 Incoming call from {current_call['name']} ({current_call['number']})")

            # Simulate ringing for 10 seconds
            ring_time = 0
            while ring_time < 10 and not user_picked:
                time.sleep(1)
                ring_time += 1

            # If user didn't answer in 10 seconds, consider missed
            if not user_picked:
                print("❌ User did not answer the call.")
            incoming = False

    call_thread = threading.Thread(target=_simulate, daemon=True)
    call_thread.start()

# -------------------------------------------------
# Check if there is an active incoming call
# -------------------------------------------------
def check_incoming_call():
    return incoming

# -------------------------------------------------
# Get current caller info
# -------------------------------------------------
def get_current_caller():
    return current_call if current_call else None

# -------------------------------------------------
# Simulate user answering manually
# -------------------------------------------------
def user_answered():
    return user_picked

# -------------------------------------------------
# For manual testing
# -------------------------------------------------
if __name__ == "__main__":
    simulate_incoming_calls()
    while True:
        if check_incoming_call():
            caller = get_current_caller()
            print(f"Detected call from {caller['name']}")
        time.sleep(2)
