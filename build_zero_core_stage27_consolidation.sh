#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

OUT="$ROOT/ZERO_CORE.consolidation.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 27 CONSOLIDATION"

jq -n --arg t "$TIME" '
{
 consolidation_version:"1.0.0",
 generated_at:$t,

 layers:[
  "core",
  "runtime",
  "authority",
  "profile",
  "event",
  "data",
  "security",
  "ai",
  "extension",
  "business",
  "release"
 ],

 duplicate_check:"READY",
 state:"CONSOLIDATED"
}
' > "$OUT"

echo "[SUCCESS] FAST STAGE 27 BUILD_SUCCESS"
