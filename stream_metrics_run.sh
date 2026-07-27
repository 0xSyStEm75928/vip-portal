#!/bin/bash

# 生成したストリームデータを Python メトリクス計算機へ渡す
echo "[*] Stream data pipeline -> Metrics Calculator"
cat input_stream.jsonl | python3 metrics_calculator.py
