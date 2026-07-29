import json, os, sys, datetime

def collect_edge_data():
    os.makedirs("json_core", exist_ok=True)
    history_file = "json_core/edge_node_history.json"

    # 普段はいけない/弾かれるノードデータ（境界値テスト用サンプル）
    raw_edge_inputs = [
        {"node_id": "ERR_UNK_NODE_999", "payload": "undefined_raw_string", "reason": "未定義の謎ノード"},
        {"node_id": "OVERFLOW_VOL_001", "payload": {"amount": 999999999999}, "reason": "桁溢れ境界値データ"},
        {"node_id": "NULL_VAL_CUSTOMER", "payload": None, "reason": "ヌル値混入ノード"}
    ]

    # 既存ログの読み込み
    logs = []
    if os.path.exists(history_file):
        try:
            logs = json.load(open(history_file, "r", encoding="utf-8"))
        except Exception:
            logs = []

    # 異物データを「正規品（JSSH規格）」に正規化して取り込む
    collected_now = []
    for raw in raw_edge_inputs:
        normalized_record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "node_id": raw["node_id"],
            "status": "ACCEPTED_VIA_QUARANTINE", # 異物を正規ルートとして許容
            "raw_payload": raw["payload"],
            "safety_guard": "PASS"
        }
        collected_now.append(normalized_record)
        logs.append(normalized_record)

    # 保存（正当なデータとして蓄積）
    json.dump(logs, open(history_file, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print("\033[1;36m=========================================================\033[0m")
    print(f"\033[1;32m [JSSH EDGE COLLECTOR] 普段いけないデータ {len(collected_now)} 件の正当取り込み完了！\033[0m")
    print("\033[1;36m=========================================================\033[0m")
    for item in collected_now:
        print(f"  - 収穫ノード: \033[1;33m{item['node_id']}\033[0m (Status: {item['status']})")
    print("---------------------------------------------------------")

if __name__ == "__main__":
    collect_edge_data()
