#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.stats.json"

echo "[*] Building Stats..."

jq '
{
 total_files:length,
 total_bytes:(map(.size)|add),
 average_bytes:((map(.size)|add)/length)
}
' "$ROOT/ZERO_CORE.index.json" > "$OUT"

echo "[OK] $OUT"
