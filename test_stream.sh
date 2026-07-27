#!/bin/bash

# 1. テスト用ストリームデータ (JSONL) の自動生成
echo "[*] Generating test stream data..."
cat << 'DATA_EOF' > input_stream.jsonl
{"id": 101, "step": "normalization", "status": "PASS", "delay_ms": 12}
{"id": 102, "step": "tokenization", "status": "PASS", "delay_ms": 45}
{"id": 103, "step": "validation", "status": "FLAGGED", "delay_ms": 300}
{"id": 104, "step": "execution", "status": "PASS", "delay_ms": 8}
DATA_EOF

echo "[+] Data saved to input_stream.jsonl"
echo ""

# 2. jq -s (slurp) を使用した配列化・集計テスト
echo "[*] Running jq stream test (-s / --slurp)..."
cat input_stream.jsonl | jq -s '
  {
    "total_records": length,
    "passed_steps": map(select(.status == "PASS")),
    "flagged_steps": map(select(.status == "FLAGGED"))
  }
' > output_summary.json

echo "[+] Stream processing complete. Summary:"
cat output_summary.json
