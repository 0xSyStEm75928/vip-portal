import json, sys, os, time

STATE_PATH = "json_core/keyboard_stream_state.json"

def load_state():
    if os.path.exists(STATE_PATH):
        try: return json.load(open(STATE_PATH, "r", encoding="utf-8"))
        except: pass
    return {"category": "BELPHEGOR_KEYBOARD", "val": 100, "last_ts": time.time(), "status": "INIT"}

def main():
    state = load_state()
    cat_title = sys.argv[1] if len(sys.argv) > 1 else "BELPHEGOR_KEYBOARD"
    
    # 1. 時間軸 (delta_ms) の計測
    now = time.time()
    last_ts = state.get("last_ts", now)
    delta_ms = int((now - last_ts) * 1000)
    state["last_ts"] = now
    state["delta_ms"] = delta_ms

    # 2. キー連打速度に応じた動的加算 (ブースト判定)
    current_val = state.get("val", 100)
    if delta_ms < 500 and delta_ms > 0: # 0.5秒以内の連打
        step = 200 # 高速連打ブースト！
        boost_flag = "BOOST_ON"
    else:
        step = 50 # 通常連打
        boost_flag = "NORMAL"

    new_val = current_val + step
    state["val"] = new_val
    state["boost"] = boost_flag

    # 3. 値に応じた動的分岐 (Branching)
    if new_val >= 1000:
        next_cat = f"{cat_title}_OVERFLOW"
    elif new_val >= 500:
        next_cat = f"{cat_title}_HIGH_GATE"
    else:
        next_cat = cat_title

    state["category"] = next_cat
    state["status"] = "KEYBOARD_STREAM_RUNNING"

    os.makedirs("json_core", exist_ok=True)
    json.dump(state, open(STATE_PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    # 次のノードへのコマンド出力
    next_cmd = f"kb_stream '{next_cat}'"
    print(f"SUCCESS|{next_cat}|{new_val}|{boost_flag}|{delta_ms}|{next_cmd}")

if __name__ == "__main__":
    main()
