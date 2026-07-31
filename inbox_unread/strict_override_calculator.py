import sys
import json
import math

def run_strict_calculator():
    raw_input = sys.stdin.read()
    if not raw_input.strip():
        print(json.dumps({"error": "Empty input stream"}, indent=2))
        return

    # 入力取得
    lines = raw_input.strip().split("\n")
    
    valid_records = []
    rejected_records = []
    delays = []
    
    # 必須スキーマ定義
    ALLOWED_STATUS = {"PASS", "FLAGGED", "FAIL"}
    
    for idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        
        try:
            record = json.loads(line)
        except Exception as e:
            rejected_records.append({"line": idx, "reason": "JSON_PARSE_ERROR", "raw": line})
            continue

        # 厳密なスキーマ検証 (Strict Schema Enforcement)
        rec_id = record.get("id")
        step = record.get("step")
        status = record.get("status")
        delay = record.get("delay_ms")

        is_valid = (
            isinstance(rec_id, int) and
            isinstance(step, str) and
            isinstance(status, str) and status in ALLOWED_STATUS and
            isinstance(delay, (int, float)) and delay >= 0
        )

        if not is_valid:
            rejected_records.append({
                "line": idx,
                "reason": "SCHEMA_VALIDATION_FAILED",
                "provided_keys": list(record.keys())
            })
            continue

        # 正常レコードを正規の厳格構造へ再定義（上書き標準化）
        normalized_record = {
            "strict_id": rec_id,
            "pipeline_step": step,
            "status": status,
            "metrics": {
                "delay_ms": delay
            }
        }
        valid_records.append(normalized_record)
        delays.append(delay)

    # 統計計算 (標準ライブラリ)
    stats = {}
    if delays:
        sorted_d = sorted(delays)
        count = len(sorted_d)
        avg_d = sum(sorted_d) / count
        min_d = sorted_d[0]
        max_d = sorted_d[-1]

        def get_p(p):
            k = (count - 1) * (p / 100.0)
            f, c = math.floor(k), math.ceil(k)
            return sorted_d[int(k)] if f == c else sorted_d[int(f)] * (c - k) + sorted_d[int(c)] * (k - f)

        stats = {
            "valid_count": count,
            "latency": {
                "avg": round(avg_d, 2),
                "min": min_d,
                "max": max_d,
                "p95": round(get_p(95), 2)
            }
        }

    # 厳格な上書き出力
    output = {
        "strict_engine_summary": {
            "total_processed_lines": len(lines),
            "status": "COMPLETED",
            "statistics": stats,
            "rejected_unknowns": {
                "count": len(rejected_records),
                "details": rejected_records
            },
            "overwritten_clean_data": valid_records
        }
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    run_strict_calculator()
