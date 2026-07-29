#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
IN="$ROOT/ZERO_CORE.30pack.json"

META="$ROOT/ZERO_CORE.30meta.json"
INDEX="$ROOT/ZERO_CORE.30index.json"
STATS="$ROOT/ZERO_CORE.30stats.json"
HASHMAP="$ROOT/ZERO_CORE.30hashmap.json"
MANIFEST="$ROOT/ZERO_CORE.30manifest.json"

echo "[*] Starting All 30-Pack Processing Tasks..."

# 1. メタデータ生成
jq '
{
  meta_version: "1.0.0",
  generated: (now|floor),
  total_files: length,
  total_bytes: (map(.bytes // 0)|add),
  total_lines: (map(.lines // 0)|add),
  schema_files: (map(select(.schema==true))|length),
  json_files: (map(select(.schema==false))|length),
  assets: .
}
' "$IN" > "$META"
echo "[OK] Generated -> $META"

# 2. インデックス生成
jq '
map({
  file,
  sha256,
  bytes: (.bytes // 0),
  lines: (.lines // 0)
})
' "$IN" > "$INDEX"
echo "[OK] Generated -> $INDEX"

# 3. 統計情報生成
jq '
{
  files: length,
  bytes: (map(.bytes // 0)|add),
  lines: (map(.lines // 0)|add),
  average_bytes: (if length > 0 then ((map(.bytes // 0)|add)/length) else 0 end),
  average_lines: (if length > 0 then ((map(.lines // 0)|add)/length) else 0 end)
}
' "$IN" > "$STATS"
echo "[OK] Generated -> $STATS"

# 4. ハッシュマップ生成
jq '
map({
  file,
  sha256
})
' "$IN" > "$HASHMAP"
echo "[OK] Generated -> $HASHMAP"

# 5. 統合マニフェスト生成
jq -n \
  --slurpfile meta "$META" \
  --slurpfile stats "$STATS" \
  --slurpfile index "$INDEX" \
  --slurpfile hashes "$HASHMAP" '
{
  manifest_version: "1.0.0",
  generated: (now|floor),
  metadata: $meta[0],
  statistics: $stats[0],
  index: $index[0],
  hashes: $hashes[0]
}
' > "$MANIFEST"

echo "=========================================="
echo "[SUCCESS] All 30-Pack Pipeline Completed!"
echo "[MANIFEST] -> $MANIFEST"
echo "=========================================="
