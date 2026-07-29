#!/bin/ash

set -eu

OUT="./json_core"
CORE="$OUT/ZERO_CORE.json"

echo "[*] Building ZERO_CORE..."

echo "[" > "$CORE"

FIRST=1

find "$OUT/json" "$OUT/schema" -type f \
    \( -name "*.json" -o -name "*.schema.json" \) \
| sort \
| while IFS= read -r FILE
do

    if jq empty "$FILE" >/dev/null 2>&1
    then

        if [ "$FIRST" -eq 0 ]; then
            echo "," >> "$CORE"
        fi

        cat "$FILE" >> "$CORE"

        FIRST=0
    fi

done

echo "]" >> "$CORE"

echo "[DONE]"
echo "$CORE"

