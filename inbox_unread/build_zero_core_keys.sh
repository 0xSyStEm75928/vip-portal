#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.keys.json"

echo "[*] Extracting JSON Keys (High-Speed)..."

find "$ROOT/json" "$ROOT/schema" -type f -name "*.json" 2>/dev/null \
| xargs -r jq -r 'paths(scalars) | map(tostring) | join(".")' 2>/dev/null \
| sort -u \
| jq -Rn '[inputs | select(length > 0) | {key: .}]' > "$OUT"

echo "[OK] $OUT"
