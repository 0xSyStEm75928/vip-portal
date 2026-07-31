#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.relationships.json"

echo "[*] Building Relationships..."

find "$ROOT/json" "$ROOT/schema" -type f -name "*.json" 2>/dev/null \
| xargs -r jq -n '
[
 inputs
 | {
     file: input_filename,
     schema:(."$schema" // null),
     version:(.version // null),
     ids:[
        .id?,
        .uuid?,
        .["@uuid"]?,
        .deal_id?,
        .kernel_id?,
        .boot_id?
     ]|map(select(.!=null))
   }
]
' > "$OUT"

echo "[OK] $OUT"
