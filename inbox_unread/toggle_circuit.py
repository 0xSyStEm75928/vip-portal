import os, sys, time, json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = os.path.join(BASE_DIR, "data_store", "circuit_state.json")

def get_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"mode": "MANUAL_AUTOMATION", "polarity": "-"}

def toggle():
    current = get_state()
    if current["mode"] == "MANUAL_AUTOMATION":
        new_state = {
            "mode": "SAAS_FULL_AUTO",
            "polarity": "+",
            "title": "🏆 [TITLE UNLOCKED] フル自動化の称号",
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        new_state = {
            "mode": "MANUAL_AUTOMATION",
            "polarity": "-",
            "title": "🏆 [TITLE UNLOCKED] オートメーション自動の称号",
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(new_state, f, ensure_ascii=False, indent=2)

    print(f"\033[1;33m[TOGGLE SWITCH]\033[0m 極性転換: \033[1;36m{current['polarity']}\033[0m ➔ \033[1;35m{new_state['polarity']}\033[0m")
    print(f"\033[1;32m[MODE]\033[0m 現在の回路状態: {new_state['mode']}")
    print(f"\033[1;34m{new_state['title']}\033[0m")
    return new_state

if __name__ == "__main__":
    toggle()
