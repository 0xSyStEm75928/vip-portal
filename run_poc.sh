#!/bin/bash

echo "========================================="
echo "  COINBASE IDOR PROOF-OF-CONCEPT RUNNER  "
echo "========================================="

# 依存ライブラリチェック
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[*] Installing required library 'requests'..."
    pip3 install requests
fi

echo "[*] Executing poc_idor.py..."
python3 poc_idor.py | tee poc_execution.log

echo ""
echo "[*] Execution log saved to 'poc_execution.log'."
