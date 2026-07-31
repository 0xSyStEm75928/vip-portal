#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.runtime.json"

echo "[*] Building Runtime..."

jq -n \
 --slurpfile stats "$ROOT/ZERO_CORE.stats.json" \
 --slurpfile versions "$ROOT/ZERO_CORE.version_report.json" \
 '{
 runtime_version:"1.0.0",
 generated:(now|floor),
 statistics:$stats[0],
 versions:$versions[0]
 }' > "$OUT"

echo "[OK] $OUT"
