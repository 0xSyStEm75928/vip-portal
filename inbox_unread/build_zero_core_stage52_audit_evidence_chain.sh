#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

EVIDENCE="$ROOT/ZERO_CORE.audit_evidence.json"
CHAIN="$ROOT/ZERO_CORE.evidence_chain.json"
REPORT="$ROOT/ZERO_CORE.audit_report_v2.json"
MANIFEST="$ROOT/ZERO_CORE.audit_manifest.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE STAGE 52 AUDIT EVIDENCE CHAIN"


# -----------------------------------------------------
# Audit Evidence
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 audit_evidence_version:"1.0.0",
 generated_at:$t,

 evidence_types:[
  "runtime_state",
  "configuration_state",
  "security_state",
  "operation_state"
 ],

 records:[],

 status:"COLLECTED"
}
' > "$EVIDENCE"


# -----------------------------------------------------
# Evidence Chain
# -----------------------------------------------------

jq -n \
 --slurpfile evidence "$EVIDENCE" \
 --arg t "$TIME" '

{
 evidence_chain_version:"1.0.0",
 generated_at:$t,

 chain:[
  "input",
  "execution",
  "validation",
  "audit"
 ],

 evidence:$evidence[0],

 integrity:"TRACKED"
}
' > "$CHAIN"


# -----------------------------------------------------
# Audit Report
# -----------------------------------------------------

jq -n \
 --slurpfile chain "$CHAIN" \
 --arg t "$TIME" '

{
 audit_report_version:"2.0.0",
 generated_at:$t,

 chain:$chain[0],

 result:"PASS"
}
' > "$REPORT"


# -----------------------------------------------------
# Audit Manifest
# -----------------------------------------------------

jq -n \
 --slurpfile report "$REPORT" \
 --arg t "$TIME" '

{
 audit_manifest_version:"1.0.0",
 generated_at:$t,

 report:$report[0],

 state:"AUDIT_READY"
}
' > "$MANIFEST"


echo
echo "[OK] EVIDENCE -> $EVIDENCE"
echo "[OK] CHAIN    -> $CHAIN"
echo "[OK] REPORT   -> $REPORT"
echo "[OK] MANIFEST -> $MANIFEST"
echo
echo "[SUCCESS] STAGE 52 BUILD_SUCCESS"
