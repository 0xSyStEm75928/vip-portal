#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

METRICS="$ROOT/ZERO_CORE.observability.json"
HEALTH="$ROOT/ZERO_CORE.health.json"
REPORT="$ROOT/ZERO_CORE.health_report.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 15"

jq -n --arg t "$TIME" '
{
 observability_version:"1.0.0",
 generated_at:$t,
 metrics:[
  "runtime",
  "events",
  "workflow",
  "security"
 ]
}
' > "$METRICS"

jq -n --arg t "$TIME" '
{
 health_version:"1.0.0",
 generated_at:$t,
 status:"HEALTHY",
 checks:[]
}
' > "$HEALTH"

jq -n \
 --slurpfile health "$HEALTH" \
 --arg t "$TIME" '
{
 health_report_version:"1.0.0",
 generated_at:$t,
 health:$health[0]
}
' > "$REPORT"

echo "[SUCCESS] FAST STAGE 15 COMPLETE"
