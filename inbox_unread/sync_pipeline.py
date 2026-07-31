import json, os, sys

BASE_DIR = "json_core"
FILES = {
    "master": os.path.join(BASE_DIR, "core_customer_master.json"),
    "ingress": os.path.join(BASE_DIR, "ingress_customer_intake.json"),
    "gate": os.path.join(BASE_DIR, "gate_lifecycle_control.json"),
    "action": os.path.join(BASE_DIR, "dispatch_next_action_queue.json"),
    "summary": os.path.join(BASE_DIR, "view_deal_sync_summary.json"),
    "quarantine": os.path.join(BASE_DIR, "quarantine_isolation_box.json") # 危険データ孤立バッファ
}

def load_j(p):
    return json.load(open(p, "r", encoding="utf-8")) if os.path.exists(p) else {}

def save_j(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

def sanitize_and_isolate(target_input):
    """【リスク位置の移動】入口で型異常・危険データを判定し、即座に孤立化させる"""
    # 型不揃いや異常入力のガード
    if not isinstance(target_input, str) or len(target_input.strip()) == 0 or "<script>" in str(target_input):
        q = load_j(FILES["quarantine"])
        q_list = q.setdefault("isolated_items", [])
        q_list.append({"raw_input": str(target_input), "reason": "DANGEROUS_OR_INVALID_TYPE", "ts": "2026-07-30T02:42:00+09:00"})
        save_j(FILES["quarantine"], q)
        return None, False # 処理中断・安全回避
    return target_input.strip(), True

def execute_safe_pipeline(target_id_raw, target_pct=100):
    ts = "2026-07-30T02:42:00+09:00"
    
    # 1. 入口での危険データ判定＆回避
    target_id, is_safe = sanitize_and_isolate(target_id_raw)
    if not is_safe:
        print(f"[⚠️ DANGER BLOCKED] 危険データ/不正入力を検知。孤立バッファ(quarantine)へ移動させパイプラインを保護しました: {target_id_raw}")
        return

    # 2. 正常データのみ後続処理（10%〜100%）へ到達
    # Master Sync
    m = load_j(FILES["master"])
    m.setdefault("customers", {})[target_id] = {"id": target_id, "status": "VERIFIED", "updated_at": ts}
    save_j(FILES["master"], m)

    # Gate Sync
    g = load_j(FILES["gate"])
    g["current_customer"] = {"id": target_id, "verified": True, "updated_at": ts}
    save_j(FILES["gate"], g)

    # Action Sync
    a = load_j(FILES["action"])
    a["tomorrow_actions"] = [{"id": target_id, "locked": True, "status": "VERIFIED"}]
    save_j(FILES["action"], a)

    # Summary Update
    s = load_j(FILES["summary"])
    s.update({"target_id": target_id, "completion_rate": f"{target_pct}%", "is_fully_confirmed": True, "risk_shield": "ACTIVE"})
    save_j(FILES["summary"], s)

    print(f"[SAFE EXECUTION COMPLETE] Target: {target_id} | Progress: {target_pct}% (Risk Shield Active)")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "CUSTOMER_001"
    pct = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    execute_safe_pipeline(target, pct)
