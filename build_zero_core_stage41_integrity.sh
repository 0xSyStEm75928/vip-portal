#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

MANIFEST="$ROOT/ZERO_CORE.integrity_manifest.json"
HASH="$ROOT/ZERO_CORE.hash_registry.json"
REPORT="$ROOT/ZERO_CORE.integrity_report.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 41 ARTIFACT INTEGRITY"


jq -n --arg t "$TIME" '
{
 integrity_manifest_version:"1.0.0",
 generated_at:$t,

 algorithm:"SHA-256",

 protected:[
  "configuration",
  "runtime",
  "security",
  "release",
  "distribution"
 ],

 status:"READY"
}
' > "$MANIFEST"


jq -n --arg t "$TIME" '
{
 hash_registry_version:"1.0.0",
 generated_at:$t,

 algorithm:"SHA-256",

 entries:[]
}
' > "$HASH"


jq -n \
 --slurpfile manifest "$MANIFEST" \
 --slurpfile hash "$HASH" \
 --arg t "$TIME" '

{
 integrity_report_version:"1.0.0",
 generated_at:$t,

 manifest:$manifest[0],
 registry:$hash[0],

 verification:"PENDING"
}
' > "$REPORT"


echo
echo "[OK] MANIFEST -> $MANIFEST"
echo "[OK] HASH     -> $HASH"
echo "[OK] REPORT   -> $REPORT"
echo
echo "[SUCCESS] FAST STAGE 41 BUILD_SUCCESS"
