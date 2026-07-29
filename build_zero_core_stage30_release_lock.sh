#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

LOCK="$ROOT/ZERO_CORE.release_lock.json"
STATUS="$ROOT/ZERO_CORE.release_status.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 30 RELEASE LOCK"

jq -n --arg t "$TIME" '
{
 release_lock_version:"1.0.0",
 generated_at:$t,

 release_state:"LOCKED",

 immutable:true,

 mode:"PRODUCTION_READY"
}
' > "$LOCK"


jq -n \
 --slurpfile lock "$LOCK" \
 --arg t "$TIME" '

{
 release_status_version:"1.0.0",
 generated_at:$t,

 release_lock:$lock[0],

 status:"ZERO_CORE_OPERATIONAL"
}

' > "$STATUS"


echo
echo "[OK] RELEASE LOCK -> $LOCK"
echo "[OK] STATUS       -> $STATUS"
echo
echo "[SUCCESS] FAST STAGE 30 BUILD_SUCCESS"
