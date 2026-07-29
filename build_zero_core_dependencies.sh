#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.dependencies.json"

echo "[*] Building Dependency Map..."

find "$ROOT/json" "$ROOT/schema" -type f -name "*.json" 2>/dev/null \
| xargs -r jq -n '
[
  inputs
  | {
      file: input_filename,
      schema: (."$schema" // null),
      references: [
        paths
        | map(tostring)
        | join(".")
      ]
    }
]
' 2>/dev/null > "$OUT"

echo "[OK] $OUT"
