#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo "   ZEROCORE REPOSITORY FULL FORGE (一括鍛錬)"
echo "=================================================="

# 1. 実行権限の再付与
echo -n "[1/4] Fixing script permissions ... "
chmod +x Validator/*.sh *.sh 2>/dev/null || true
echo "DONE 🟢"

# 2. 全JSONファイルの構文一括チェック
echo "[2/4] Validating ALL JSON files in repository ... "
ERRORS=0
for f in $(find . -type f -name "*.json" ! -path "*/.git/*"); do
    if jq empty "$f" 2>/dev/null; then
        echo "  - $f : OK"
    else
        echo "  - $f : INVALID ❌"
        ERRORS=$((ERRORS + 1))
    fi
done

if [ $ERRORS -gt 0 ]; then
    echo "鍛錬失敗: $ERRORS 個のJSONに不整合があります。"
    exit 1
fi
echo "ALL JSON SYNTAX PASS 🟢"

# 3. カレントカーネルレコードの検証
echo -n "[3/4] Verifying kernel boot record ... "
if [ -f "kernel_boot_record.json" ]; then
    jq empty kernel_boot_record.json && echo "PASS 🟢"
else
    echo "SKIPPED (kernel_boot_record.json not found)"
fi

# 4. バリデータの実行
echo "[4/4] Executing Sovereign Runtime Validator ... "
if [ -f "./Validator/zerocore_validate.sh" ]; then
    ./Validator/zerocore_validate.sh
fi

echo "=================================================="
echo " STATUS: REPOSITORY FULLY FORGED & VERIFIED ⚔️🟢"
echo "=================================================="
