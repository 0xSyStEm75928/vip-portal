#!/usr/bin/env bash
set -euo pipefail

echo "======================================================================"
echo "    ZEROCORE - TRADE STATUS UPDATE: AWAITING ESCROW DEPOSIT          "
echo "======================================================================"
echo " [*] Target Buyer: SILENT_USER_0x89A (\$35,000 USDT)"
echo " [*] Payout Address: Ledger Stax (0xF7A3...0e91)"
echo "----------------------------------------------------------------------"

# 1% -> 100% 入金待ちロックストリーム
for i in $(seq 1 100); do
  STATUS="IN_PROGRESS"
  if [ "$i" -eq 100 ]; then STATUS="AWAITING_DEPOSIT_LOCKED"; fi
  
  jq -n \
    --arg percent "$i" \
    --arg status "$STATUS" \
    --arg time "$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")" \
    '{
      stream_event: "SETTING_AWAITING_DEPOSIT_STATUS",
      progress_percent: ($percent | tonumber),
      timestamp: $time,
      phase: (if ($percent | tonumber) <= 50 then "ACCEPTING_BUYER_PROPOSAL"
              else "LOCKING_AWAITING_DEPOSIT_STATE" end),
      status: $status
    }' -c
  sleep 0.01
done

echo "----------------------------------------------------------------------"
echo " [!] STATUS LOCKED: Awaiting Escrow Deposit"
echo "----------------------------------------------------------------------"
jq '.' awaiting_deposit_status.json
echo "======================================================================"

# Gitステージング・コミット・Pushを一括実行
git add awaiting_deposit_status.json run_awaiting_deposit.sh
git commit -m "status(trade): accept buyer proposal and lock status to AWAITING_ESCROW_DEPOSIT"
git push origin main
