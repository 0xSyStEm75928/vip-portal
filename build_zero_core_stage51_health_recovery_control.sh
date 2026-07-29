#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

HEALTH="$ROOT/ZERO_CORE.health_control.json"
RECOVERY="$ROOT/ZERO_CORE.recovery_control.json"
INCIDENT="$ROOT/ZERO_CORE.incident_state.json"
MANIFEST="$ROOT/ZERO_CORE.health_manifest.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE STAGE 51 HEALTH / RECOVERY CONTROL"


jq -n --arg t "$TIME" '
{
 health_control_version:"1.0.0",
 generated_at:$t,

 checks:[
  "runtime",
  "integrity",
  "configuration",
  "availability"
 ],

 status:"HEALTH_READY"
}
' > "$HEALTH"


jq -n --arg t "$TIME" '
{
 recovery_control_version:"1.0.0",
 generated_at:$t,

 recovery_modes:[
  "snapshot_restore",
  "configuration_restore",
  "archive_restore"
 ],

 status:"RECOVERY_READY"
}
' > "$RECOVERY"


jq -n --arg t "$TIME" '
{
 incident_state_version:"1.0.0",
 generated_at:$t,

 current_state:"NORMAL",

 incidents:[],

 monitoring:"ENABLED"
}
' > "$INCIDENT"


jq -n \
 --slurpfile health "$HEALTH" \
 --slurpfile recovery "$RECOVERY" \
 --slurpfile incident "$INCIDENT" \
 --arg t "$TIME" '
{
 health_manifest_version:"1.0.0",
 generated_at:$t,

 health:$health[0],
 recovery:$recovery[0],
 incident:$incident[0],

 state:"PROTECTED"
}
' > "$MANIFEST"


echo
echo "[OK] HEALTH    -> $HEALTH"
echo "[OK] RECOVERY  -> $RECOVERY"
echo "[OK] INCIDENT  -> $INCIDENT"
echo "[OK] MANIFEST  -> $MANIFEST"
echo
echo "[SUCCESS] STAGE 51 BUILD_SUCCESS"
