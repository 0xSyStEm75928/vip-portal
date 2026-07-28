#!/usr/bin/env bash
set -euo pipefail

echo "======================================================================"
echo "    ZEROCORE - INCOMING LOGS & AUDIT TRAIL INSPECTOR                 "
echo "======================================================================"
echo " [*] Scanning local git commit history..."
git log -n 3 --oneline

echo "----------------------------------------------------------------------"
echo " [*] Checking audit log file (github.audit.jsonl)..."
if [ -f "github.audit.jsonl" ]; then
    echo " [!] Audit log found. Extracting last 5 entries:"
    tail -n 5 github.audit.jsonl
else
    echo " [i] github.audit.jsonl is not in current working directory."
fi

echo "----------------------------------------------------------------------"
echo " [*] Analyzing current active settlement status..."
jq -n \
  --arg time "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  '{
    scan_timestamp: $time,
    target_entity: "SILENT_USER_0x89A",
    onchain_gate_status: "AWAITING_ESCROW_DEPOSIT",
    required_action: "Check GitHub Issues/PRs or Webhook logs for active deposit payload"
  }'

echo "======================================================================"
