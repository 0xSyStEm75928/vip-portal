#!/bin/ash
#
# ZeroCore JSON Core Extractor
# Alpine / BusyBox ash
#

set -eu

ROOT="${1:-.}"

OUTDIR="./json_core"
mkdir -p "$OUTDIR"

echo "[*] Searching JSON / JSONL..."

find "$ROOT" \
    \( -name "*.json" -o -name "*.jsonl" -o -name "*.schema.json" \) \
    | sort > "$OUTDIR/filelist.txt"

echo "[*] Collecting metadata..."

: > "$OUTDIR/core.index.jsonl"

while IFS= read -r file
do
    if jq empty "$file" >/dev/null 2>&1
    then
        HASH=$(sha256sum "$file" | awk '{print $1}')
        SIZE=$(wc -c < "$file")

        jq -n \
          --arg file "$file" \
          --arg hash "$HASH" \
          --argjson size "$SIZE" \
          '{
            file:$file,
            sha256:$hash,
            size:$size
          }' >> "$OUTDIR/core.index.jsonl"
    else
        echo "[WARN] Invalid JSON: $file"
    fi
done < "$OUTDIR/filelist.txt"

echo "[*] Extracting schema paths..."

: > "$OUTDIR/schema.paths"

grep -Rh '"\$schema"' "$ROOT" 2>/dev/null \
| sed 's/^[^:]*://' \
| sort -u \
> "$OUTDIR/schema.paths" || true

echo "[*] Extracting versions..."

: > "$OUTDIR/version.index"

grep -Rh '"version"' "$ROOT" 2>/dev/null \
| sort -u \
> "$OUTDIR/version.index" || true

echo "[*] Extracting ids..."

: > "$OUTDIR/id.index"

grep -Rh '"id"\|"deal_id"\|"boot_id"\|"kernel_id"\|"uuid"' "$ROOT" 2>/dev/null \
| sort -u \
> "$OUTDIR/id.index" || true

echo
echo "[OK] JSON Core Extracted"
echo
echo "Output:"
echo "  $OUTDIR/filelist.txt"
echo "  $OUTDIR/core.index.jsonl"
echo "  $OUTDIR/schema.paths"
echo "  $OUTDIR/version.index"
echo "  $OUTDIR/id.index"
