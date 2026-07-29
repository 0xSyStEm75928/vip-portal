#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.hashes.json"

echo "[*] Building Hash Map (Ultra-Fast)..."

find "$ROOT/json" "$ROOT/schema" -type f -name "*.json" 2>/dev/null \
| xargs -r sha256sum \
| awk '{print $2 "\t" $1}' \
| jq -Rn '
[
    inputs
    | split("\t")
    | {
        file: .[0],
        sha256: .[1]
    }
]
' > "$OUT"

echo "[OK] $OUT"
