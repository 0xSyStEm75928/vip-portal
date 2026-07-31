#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.integrity.json"

echo "[*] Building Integrity..."

jq -n \
 --slurpfile hashes "$ROOT/ZERO_CORE.hashes.json" \
 --slurpfile ids "$ROOT/ZERO_CORE.ids.json" '
{
 generated:(now|floor),
 hashes:$hashes[0],
 ids:$ids[0]
}
' > "$OUT"

echo "[OK] $OUT"
