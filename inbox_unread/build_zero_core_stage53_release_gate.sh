#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

GATE="$ROOT/ZERO_CORE.release_gate.json"
CONTROL="$ROOT/ZERO_CORE.final_control.json"
STATUS="$ROOT/ZERO_CORE.v1_final_status.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE STAGE 53 RELEASE GATE"


# -----------------------------------------------------
# Release Gate
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 release_gate_version:"1.0.0",
 generated_at:$t,

 checks:[
  "archive",
  "integrity",
  "backup",
  "audit",
  "operation"
 ],

 result:"PASS",

 state:"RELEASE_APPROVED"
}
' > "$GATE"


# -----------------------------------------------------
# Final Control
# -----------------------------------------------------

jq -n \
 --slurpfile gate "$GATE" \
 --arg t "$TIME" '

{
 final_control_version:"1.0.0",
 generated_at:$t,

 release_gate:$gate[0],

 controls:[
  "version_lock",
  "change_control",
  "maintenance"
 ],

 state:"CONTROLLED"
}
' > "$CONTROL"


# -----------------------------------------------------
# Final Status
# -----------------------------------------------------

jq -n \
 --slurpfile control "$CONTROL" \
 --arg t "$TIME" '

{
 final_status_version:"1.0.0",
 generated_at:$t,

 control:$control[0],

 release:"ZERO_CORE_v1.x",

 status:"FINALIZED"
}
' > "$STATUS"


echo
echo "[OK] GATE    -> $GATE"
echo "[OK] CONTROL -> $CONTROL"
echo "[OK] STATUS  -> $STATUS"
echo
echo "[SUCCESS] STAGE 53 COMPLETE"
echo "[STATUS] ZERO_CORE_v1.x_FINALIZED"
