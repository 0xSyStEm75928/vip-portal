import json, sys, os, math, datetime

STATE_PATH = "json_core/belphegor_qa_state.json"

def load_state():
    if os.path.exists(STATE_PATH):
        try: return json.load(open(STATE_PATH, "r", encoding="utf-8"))
        except: pass
    return {"cycle_count": 0, "current_phase": "QUESTION", "radical_entropy": 0.85}

def save_state(data):
    os.makedirs("json_core", exist_ok=True)
    json.dump(data, open(STATE_PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

def main():
    state = load_state()
    cycle = state.get("cycle_count", 0) + 1
    phase = state.get("current_phase", "QUESTION")
    entropy = state.get("radical_entropy", 0.85)

    ts = datetime.datetime.now().isoformat()
    if phase == "QUESTION":
        payload = {
            "type": "AUTO_QUESTION", "cycle": cycle, "timestamp": ts,
            "question_id": f"Q_{cycle:03d}",
            "text": f"【過激問 {cycle}】ボトルネック B_{cycle} の整合性を破綻させずに最大化せよ",
            "action": "GENERATE_ANSWER"
        }
        next_phase = "ANSWER"
    else:
        conf = round(1.0 / (1.0 + math.exp(-0.2 * (entropy * 50 - 20))), 4)
        payload = {
            "type": "AUTO_ANSWER", "cycle": cycle, "timestamp": ts,
            "answer_id": f"A_{cycle:03d}", "confidence": conf,
            "hypothesis": f"【過激答 {cycle}】EMA平滑化＋Sigmoid確率({round(conf*100,1)}%)で強制突破",
            "action": "GENERATE_QUESTION"
        }
        next_phase = "QUESTION"

    new_entropy = min(0.99, max(0.50, entropy + (0.02 if phase == "QUESTION" else -0.01)))
    state.update({"cycle_count": cycle, "current_phase": next_phase, "radical_entropy": round(new_entropy, 4), "last_qa": payload})
    save_state(state)
    print(f"SUCCESS|{payload['type']}|{cycle}")

if __name__ == "__main__":
    main()
