#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.ids.json"

echo "[*] Building ID Map (Ultra-Fast)..."

find "$ROOT/json" "$ROOT/schema" -type f -name "*.json" 2>/dev/null \
| xargs -r jq -n '
[
    inputs
    | {
        file: input_filename,
        id: (.id // null),
        uuid: (.uuid // .["@uuid"] // null),
        deal_id: (.deal_metadata.deal_id // .deal_id // null),
        kernel_id: (.kernel.kernel_id // .kernel_id // null),
        boot_id: (.boot.boot_id // .boot_id // null)
    }
]
' 2>/dev/null > "$OUT"

echo "[OK] $OUT"
