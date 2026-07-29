#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

API="$ROOT/ZERO_CORE.api.json"
CLI="$ROOT/ZERO_CORE.cli.json"
HOOK="$ROOT/ZERO_CORE.webhook.json"
EXPORT="$ROOT/ZERO_CORE.interface_export.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 11"

jq -n --arg t "$TIME" '
{
 api_version:"1.0.0",
 generated_at:$t,
 endpoints:[],
 auth:"ZERO_CORE_POLICY"
}
' > "$API"

jq -n --arg t "$TIME" '
{
 cli_version:"1.0.0",
 generated_at:$t,
 command:"sun",
 commands:[
  "status",
  "audit",
  "export",
  "workflow"
 ]
}
' > "$CLI"

jq -n --arg t "$TIME" '
{
 webhook_version:"1.0.0",
 generated_at:$t,
 listeners:[]
}
' > "$HOOK"

jq -n \
 --slurpfile api "$API" \
 --slurpfile cli "$CLI" \
 --arg t "$TIME" '
{
 interface_export_version:"1.0.0",
 generated_at:$t,
 api:$api[0],
 cli:$cli[0]
}
' > "$EXPORT"

echo "[SUCCESS] FAST STAGE 11 COMPLETE"
