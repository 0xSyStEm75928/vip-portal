#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.versions.json"

echo "[*] Building Version Map (Ultra-Fast)..."

find "$ROOT/json" "$ROOT/schema" -type f -name "*.json" 2>/dev/null \
| xargs -r jq -n '[inputs | {file: input_filename, version: (.version // null), schema: (."$schema" // null)}]' 2>/dev/null > "$OUT"

echo "[OK] $OUT"
