#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.diff.json"

echo "[*] Building Diff Map..."

jq -n \
  --slurpfile idx "$ROOT/ZERO_CORE.index.json" \
  --slurpfile hash "$ROOT/ZERO_CORE.hashes.json" '
{
  generated:(now|floor),
  files:$idx[0],
  hashes:$hash[0]
}
' > "$OUT"

echo "[OK] $OUT"
