#!/bin/bash

echo "===================================================="
echo " [PIRDAG TRIAGE PROTOCOL] CHECKING NODE STATUS..."
echo "===================================================="

# 1. 匿名ローカル設定の自動強制適用
git config --local user.name "Node-Anonymous"
git config --local user.email "node-anonymous@users.noreply.github.com"
echo "[✓] Local Anonymous Profile Enforcement: SUCCESS"

# 2. 個人ポータブルハッシュの判定・生成
if [ ! -f "my_portable_hash.json" ]; then
    echo "[!] Portable Hash Missing. Generating new node key..."
    HASH_VAL=$(echo "Node_$(date +%s)_$RANDOM" | sha256sum | awk '{print $1}')
    echo "{\"portable_hash\": \"0x$HASH_VAL\", \"role\": \"GOVERNANCE_NODE\"}" > my_portable_hash.json
    echo "[✓] Personal Portable Hash Created: 0x$HASH_VAL"
else
    echo "[✓] Personal Portable Hash Detected."
fi

# 3. 傘下ツリー（GENESIS_HASH_TREE）の疎通確認
if [ -f "GENESIS_HASH_TREE.json" ]; then
    echo "[✓] Genesis Tree Alignment: CONNECTED"
else
    echo "[!] Tree missing. Force pulling from main..."
    git pull origin main --rebase > /dev/null 2>&1
fi

echo "===================================================="
echo " [TRIAGE COMPLETE] You are fully elevated."
echo " Run './chat.sh read' to view governance log."
echo "===================================================="
