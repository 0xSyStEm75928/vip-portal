import json, os, hashlib, time

BASE_DIR          = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_PATH        = os.path.join(BASE_DIR, "data_store", "active_state.json")
TREND_NDJSON_PATH = os.path.join(BASE_DIR, "data_store", "stream_events.ndjson")

def main():
    now = time.time()
    iso_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))

    new_state = {
        "timestamp": iso_time,
        "status": "OPERATIONAL_CLEAN",
        "engine": "integrity_engine_v2"
    }
    
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, 'w', encoding='utf-8') as f:
        json.dump(new_state, f, indent=2, ensure_ascii=False)

    trend_event = {
        "event_id": f"evt_{int(now*1000)}",
        "@timestamp": iso_time,
        "status": "PULSE_OK"
    }
    with open(TREND_NDJSON_PATH, "a", encoding="utf-8") as ndf:
        ndf.write(json.dumps(trend_event, ensure_ascii=False) + "\n")

    print("\033[1;32m[ENGINE RUN]\033[0m 最新の状態を更新し、NDJSONログに追記しました。")

if __name__ == "__main__":
    main()
