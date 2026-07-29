#!/bin/ash
set -eu
ROOT="${1:-./json_core}"
INDEX="$ROOT/ZERO_CORE.index.json"

echo "[*] Building ZERO_CORE Index (High-Speed)..."

find "$ROOT" -type f \( -name "*.json" -o -name "*.schema.json" -o -name "*.jsonl" \) \
| sort \
| xargs -r sha256sum \
| awk '{print $2 "\t" $1}' \
| while IFS=$'\t' read -r FILE SHA; do
    SIZE=$(wc -c < "$FILE" | tr -d ' ')
    echo "$FILE $SHA $SIZE"
  done \
| jq -Rn '
  [inputs | split(" ") | {
    file: .[0],
    sha256: .[1],
    size: (.[2] | tonumber)
  }]
' > "$INDEX"

echo "[OK] $INDEX"
