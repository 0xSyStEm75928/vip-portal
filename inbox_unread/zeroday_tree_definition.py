import sys
import json

def evaluate_zeroday_tree(lines):
    tree_results = {
        "tree_summary": {
            "node_type": "ROOT_ZERO_DAY_CLASSIFIER",
            "branches": {
                "NORMAL_PASS": [],          # 完全な正常データ
                "STRICT_REJECTED": [],      # 単純な型エラー・拒否データ
                "ZERO_DAY_CANDIDATE": []    # 『ノーマルを装った空白』潜伏データ
            }
        }
    }

    for idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except Exception:
            continue

        rec_id = data.get("id")
        status = data.get("status")
        delay = data.get("delay_ms", 0)
        keys_count = len(data.keys())

        # ツリー分岐判定ロジック
        # 分岐1: 必須キーを満たし、見た目はPASSだが『情報の詰め込み(Overstuffed keys > 5)』または『時間ギャップ(delay > 200ms)』を持つ場合
        if status == "PASS" and (keys_count > 5 or delay > 200):
            tree_results["tree_summary"]["branches"]["ZERO_DAY_CANDIDATE"].append({
                "line": idx,
                "id": rec_id,
                "vector": "GHOST_GAP_OR_OVERSTUFFED_PAYLOAD",
                "risk_score": "CRITICAL",
                "details": f"Keys: {keys_count}, Delay: {delay}ms"
            })
        # 分岐2: 通常の正常処理
        elif isinstance(rec_id, int) and status in ["PASS", "FLAGGED"] and keys_count <= 5:
            tree_results["tree_summary"]["branches"]["NORMAL_PASS"].append({
                "line": idx,
                "id": rec_id,
                "status": status
            })
        # 分岐3: 拒否対象
        else:
            tree_results["tree_summary"]["branches"]["STRICT_REJECTED"].append({
                "line": idx,
                "reason": "SCHEMA_MISMATCH_OR_OUT_OF_BOUNDS"
            })

    print(json.dumps(tree_results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    evaluate_zeroday_tree(lines)
