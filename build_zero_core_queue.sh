#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.queue.json"

echo "[*] Building Rewrite Queue..."

jq '
map({
  file,
  status:"PENDING"
})
' "$ROOT/ZERO_CORE.index.json" > "$OUT"

echo "[OK] $OUT"
