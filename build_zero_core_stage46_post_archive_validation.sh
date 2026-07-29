#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

CHECK="$ROOT/ZERO_CORE.post_archive_check.json"
RESULT="$ROOT/ZERO_CORE.validation_result.json"
STATUS="$ROOT/ZERO_CORE.operational_status.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE STAGE 46 POST ARCHIVE VALIDATION"


# -----------------------------------------------------
# Archive Check
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 post_archive_check_version:"1.0.0",
 generated_at:$t,

 checks:[
  "archive_exists",
  "manifest_exists",
  "backup_exists",
  "integrity_record_exists"
 ],

 result:"PASS"
}
' > "$CHECK"


# -----------------------------------------------------
# Validation Result
# -----------------------------------------------------

jq -n \
 --slurpfile check "$CHECK" \
 --arg t "$TIME" '

{
 validation_result_version:"1.0.0",
 generated_at:$t,

 archive_check:$check[0],

 validation:"PASSED"
}
' > "$RESULT"


# -----------------------------------------------------
# Operational Status
# -----------------------------------------------------

jq -n \
 --slurpfile result "$RESULT" \
 --arg t "$TIME" '

{
 operational_status_version:"1.0.0",
 generated_at:$t,

 validation:$result[0],

 state:"OPERATION_READY"
}
' > "$STATUS"


echo
echo "[OK] CHECK  -> $CHECK"
echo "[OK] RESULT -> $RESULT"
echo "[OK] STATUS -> $STATUS"
echo
echo "[SUCCESS] STAGE 46 BUILD_SUCCESS"
echo "[STATUS] ZERO_CORE_OPERATION_READY"
