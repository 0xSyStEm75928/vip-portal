#!/usr/bin/env bash
set -euo pipefail

# ----------------------------------------------------------------------
# Real-data Prospect Filter Engine
# ※ テストデータ・ダミーの自動生成は一切行いません。
#    入力された実ログ（JSON/CSV/TSV）から条件に合う積極客のみを抽出します。
# ----------------------------------------------------------------------

INPUT_LOG=${1:-""}

if [ -z "$INPUT_LOG" ] || [ ! -f "$INPUT_LOG" ]; then
  echo "【エラー】検品対象の実際のログファイル（JSON）を指定してください。"
  echo "使用例: ./filter_active_buyers.sh <実アクセスログファイル.json>"
  exit 1
fi

echo "======================================================================"
echo "    REAL BUYER INSPECTOR : ACTIVE INTENT AUDIT                        "
echo "======================================================================"
echo " [*] Target File: ${INPUT_LOG}"
echo " [*] Filtering criteria: (Direct Request / High View Count / Explicit Code Intent)"
echo "----------------------------------------------------------------------"

# 実際のログから「コード要求・高意欲（HIGH/EXPLICIT）」の客だけを抽出して表示
jq '
  if type == "array" then . else [.[]] end
  | map(select(
      (.action == "REQUEST_CODE" or .action == "BUY_INTENT" or .intent == "HIGH" or .intent == "EXPLICIT")
      and (.is_bot != true)
    ))
  | {
      total_active_buyers: length,
      qualified_clients: .
    }
' "$INPUT_LOG"

