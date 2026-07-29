#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
IN="$ROOT/ZERO_CORE.30pack.json"
OUT="$ROOT/ZERO_CORE.30stats.json"

echo "[*] Building 30-Pack Stats..."

jq '
{
  files:length,
  bytes:(map(.bytes)|add),
  lines:(map(.lines)|add),
  average_bytes:((map(.bytes)|add)/length),
  average_lines:((map(.lines)|add)/length)
}
' "$IN" > "$OUT"

echo "[OK] $OUT"
