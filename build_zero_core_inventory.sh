#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.inventory.json"

echo "[*] Building Inventory..."

jq -n \
    --slurpfile idx "$ROOT/ZERO_CORE.index.json" \
    --slurpfile stats "$ROOT/ZERO_CORE.stats.json" \
    --slurpfile ver "$ROOT/ZERO_CORE.version_report.json" \
    --slurpfile schema "$ROOT/ZERO_CORE.schema_report.json" '
{
 inventory_version:"1.0.0",
 files:$idx[0],
 statistics:$stats[0],
 versions:$ver[0],
 schemas:$schema[0]
}
' > "$OUT"

echo "[OK] $OUT"
