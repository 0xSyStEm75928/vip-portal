#!/usr/bin/env bash
set -euo pipefail

echo "======================================================================"
echo "      ZEROCORE REPOSITORY - FILE CONSOLIDATION ANALYSIS               "
echo "======================================================================"

echo "1. ディレクトリ別のJSONファイル数:"
find . -type f -name "*.json" ! -path "*/.git/*" ! -path "*/node_modules/*" | awk -F'/' '{print $2}' | sort | uniq -c | sort -nr

echo -e "\n2. 重複（完全一致または類似）している可能性が高いファイル構造:"
find . -type f -name "*.json" ! -path "*/.git/*" ! -path "*/node_modules/*" -exec jq -r 'keys | sort | join(",")' {} + 2>/dev/null | sort | uniq -c | sort -nr | head -n 10

