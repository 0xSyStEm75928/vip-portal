import json, os, sys, subprocess

BASE_DIR = "json_core"

# --- DAG 依存関係グラフ定義 (Node Dependencies) ---
DAG_GRAPH = {
    "N1_INGRESS":  {"file": f"{BASE_DIR}/ingress_customer_intake.json", "deps": []},
    "N2_MASTER":   {"file": f"{BASE_DIR}/core_customer_master.json", "deps": ["N1_INGRESS"]},
    "N3_GATE":     {"file": f"{BASE_DIR}/gate_lifecycle_control.json", "deps": ["N2_MASTER"]},
    "N4_ACTION":   {"file": f"{BASE_DIR}/dispatch_next_action_queue.json", "deps": ["N3_GATE"]},
    "N5_SUMMARY":  {"file": f"{BASE_DIR}/view_deal_sync_summary.json", "deps": ["N4_ACTION"]}
}

def load_j(p):
    return json.load(open(p, "r", encoding="utf-8")) if os.path.exists(p) else {}

def save_j(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

def propagate_dag(target_id, start_node="N1_INGRESS"):
    """指定されたノードからDAGの依存関係に沿って後続を連動（チェーン）更新する"""
    ts = "2026-07-30T02:44:00+09:00"
    
    print("="*60)
    print(f" [DAG CHAIN TRIGGER] Node: {start_node} -> Propagating downstream...")
    print("="*60)

    # 1. 依存連動ロジック
    nodes_to_run = ["N1_INGRESS", "N2_MASTER", "N3_GATE", "N4_ACTION", "N5_SUMMARY"]
    start_idx = nodes_to_run.index(start_node) if start_node in nodes_to_run else 0
    active_chain = nodes_to_run[start_idx:]

    for node in active_chain:
        fpath = DAG_GRAPH[node]["file"]
        data = load_j(fpath)
        
        # 連動更新ロジック
        data["dag_node"] = node
        data["target_id"] = target_id
        data["chain_status"] = "SYNCED_VIA_DAG"
        data["updated_at"] = ts
        
        save_j(fpath, data)
        print(f"  ├─► [DAG NODE LOCKED] {node:<12} -> File: {fpath}")

    # 2. history -s に連動コマンド群をバッチ調律インジェクション
    history_cmds = [
        f"python3 dag_history_trigger.py {target_id} N1_INGRESS",
        f"python3 dag_history_trigger.py {target_id} N3_GATE",
        f"python3 dag_history_trigger.py {target_id} N5_SUMMARY",
        f"jq .chain_status {DAG_GRAPH['N5_SUMMARY']['file']}"
    ]
    
    # シェル履歴へ注入
    for cmd in history_cmds:
        subprocess.run(f'history -s "{cmd}"', shell=True, executable='/bin/bash')

    print("="*60)
    print(f">>> DAG PROPAGATION COMPLETE: {len(active_chain)} Nodes Auto-Linked <<<")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "CUSTOMER_001"
    node = sys.argv[2] if len(sys.argv) > 2 else "N1_INGRESS"
    propagate_dag(target, node)
