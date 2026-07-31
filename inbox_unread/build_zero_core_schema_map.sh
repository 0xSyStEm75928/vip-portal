#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.schema_map.json"

echo "[*] Building Schema Map (High-Speed)..."

find "$ROOT/json" "$ROOT/schema" -type f -name "*.json" 2>/dev/null \
| xargs -r jq -c '{file: input_filename, schema: (."$schema" // null)}' 2>/dev/null \
| jq -s '.' > "$OUT"

echo "[OK] $OUT"
