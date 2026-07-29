#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.30pack.json"

echo "[*] Processing 30-Asset JSON Bundle (Ultra-Fast Stream)..."

find "$ROOT" -type f \( -name "*.json" -o -name "*.schema.json" -o -name "*.jsonl" \) 2>/dev/null \
| sort \
| head -n 30 \
| xargs -r sha256sum \
| awk '{print $2 "\t" $1}' \
| while IFS=$'\t' read -r FILE SHA; do
    SIZE=$(wc -c < "$FILE" | tr -d ' ')
    LINES=$(wc -l < "$FILE" | tr -d ' ')
    echo "$FILE $SHA $SIZE $LINES"
  done \
| jq -Rn '
[
  inputs | split(" ") | {
    file: .[0],
    sha256: .[1],
    bytes: (.[2] | tonumber),
    lines: (.[3] | tonumber),
    schema: (if .[0] | endswith(".schema.json") then true else false end)
  }
]
' > "$OUT"

echo "[OK] Generated 30-Pack JSON -> $OUT"
