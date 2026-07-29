#!/bin/ash
#
# ZeroCore JSON Collector
# Alpine / BusyBox ash
#

set -eu

ROOT="${1:-.}"

OUT="./json_core"

mkdir -p \
"$OUT/json" \
"$OUT/schema" \
"$OUT/jsonl"

echo "[*] Collecting JSON..."

find "$ROOT" -type f -name "*.json" | while IFS= read -r FILE
do
    DEST="$OUT/json/$(basename "$FILE")"

    if [ ! -f "$DEST" ]; then
        cp "$FILE" "$DEST"
    fi
done

echo "[*] Collecting Schema..."

find "$ROOT" -type f -name "*.schema.json" | while IFS= read -r FILE
do
    DEST="$OUT/schema/$(basename "$FILE")"

    if [ ! -f "$DEST" ]; then
        cp "$FILE" "$DEST"
    fi
done

echo "[*] Collecting JSONL..."

find "$ROOT" -type f -name "*.jsonl" | while IFS= read -r FILE
do
    DEST="$OUT/jsonl/$(basename "$FILE")"

    if [ ! -f "$DEST" ]; then
        cp "$FILE" "$DEST"
    fi
done

echo "[*] Building Manifest..."

find "$OUT" -type f \
| sort \
> "$OUT/MANIFEST.txt"

echo "[DONE]"
echo
echo "$OUT"
