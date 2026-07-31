#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
IN="$ROOT/ZERO_CORE.30pack.json"
OUT="$ROOT/ZERO_CORE.30hashmap.json"

echo "[*] Building 30-Pack Hash Map..."

jq '
map({
  file,
  sha256
})
' "$IN" > "$OUT"

echo "[OK] $OUT"
