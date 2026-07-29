#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.catalog.json"

echo "[*] Building Catalog..."

jq '
map({
 file,
 size,
 sha256
})
' "$ROOT/ZERO_CORE.index.json" > "$OUT"

echo "[OK] $OUT"
