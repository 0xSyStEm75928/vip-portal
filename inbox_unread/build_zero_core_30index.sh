#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
IN="$ROOT/ZERO_CORE.30pack.json"
OUT="$ROOT/ZERO_CORE.30index.json"

echo "[*] Building 30-Pack Index..."

jq '
map({
  file,
  sha256,
  bytes,
  lines
})
' "$IN" > "$OUT"

echo "[OK] $OUT"
