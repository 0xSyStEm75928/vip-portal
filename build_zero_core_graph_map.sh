#!/bin/ash
# ----------------------------------------------------------------------
# ZERO_CORE Graph Map Builder (Authority / Canonical Edition)
# ----------------------------------------------------------------------
set -eu

ROOT="${1:-./json_core}"
OUT="$ROOT/ZERO_CORE.graph_map.json"

if [ ! -d "$ROOT" ]; then
    echo "[ERROR] Target directory '$ROOT' does not exist." >&2
    exit 1
fi

echo "[*] Building Graph Map (Canonical Mode)..."

TMP_STREAM="$(mktemp)"

# ファイル収集と個別要素解析（壊れたJSONの孤立エラーハンドリング）
find "$ROOT" -type f -name "*.json" 2>/dev/null | sort | while IFS= read -r FILE; do
    # JSONのバリデーション兼グラフノードデータ抽出
    jq -c --arg file "$FILE" '
        try {
            file: $file,
            schema: (."$schema" // null),
            version: (.version // null),
            type: (if ."$schema" != null then "schema" else "data" end),
            keys_count: (keys | length),
            references: (
                [ .. | strings | select(test("\\.json$")) ] 
                | unique
            )
        } catch {
            file: $file,
            error: "INVALID_JSON",
            schema: null,
            version: null,
            references: []
        }
    ' "$FILE" >> "$TMP_STREAM"
done

# 解析ストリームを厳密なJSON構造（配列表現およびメタデータ付き）に整形
jq -s --arg generated_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '
    {
        authority_version: "1.0.0",
        generated_at: $generated_at,
        total_nodes: length,
        valid_nodes: (map(select(.error == null)) | length),
        invalid_nodes: (map(select(.error != null)) | length),
        graph: .
    }
' "$TMP_STREAM" > "$OUT"

rm -f "$TMP_STREAM"

echo "[OK] Graph Map Built Successfully -> $OUT"
