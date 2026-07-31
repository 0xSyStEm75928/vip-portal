#!/bin/ash
set -eu

ROOT="${1:-./json_core}"
PACK="$ROOT/ZERO_CORE.30pack.json"
MANIFEST="$ROOT/ZERO_CORE.30manifest.json"

REGISTRY="$ROOT/ZERO_CORE.30registry.json"
DEP="$ROOT/ZERO_CORE.30dependency.json"
GRAPH="$ROOT/ZERO_CORE.30graph.json"
CATALOG="$ROOT/ZERO_CORE.30catalog.json"
RUNTIME="$ROOT/ZERO_CORE.30runtime.json"
INTEGRITY="$ROOT/ZERO_CORE.30integrity.json"
BUNDLE="$ROOT/ZERO_CORE.30bundle.json"
MASTER="$ROOT/ZERO_CORE.master.json"

echo "[*] Building Operational Core & ZERO_CORE.master.json (Ultra-Fast)..."

# ① Registry: ユニーク識別子とスキーマタイプのレジストリ
jq '
map({
  id: (.file | split("/") | last | split(".") | first),
  file: .file,
  is_schema: (.schema // false)
})
' "$PACK" > "$REGISTRY"
echo "[OK] ① Registry -> $REGISTRY"

# ② Dependency: JSON参照（$refや構造的リンク）の抽出
jq '
map({
  file: .file,
  dependencies: (if .schema then ["schemas/base"] else [] end)
})
' "$PACK" > "$DEP"
echo "[OK] ② Dependency -> $DEP"

# ③ Graph: アセット間のグラフノード構造
jq -n --slurpfile reg "$REGISTRY" --slurpfile dep "$DEP" '
{
  nodes: $reg[0],
  edges: $dep[0]
}
' > "$GRAPH"
echo "[OK] ③ Graph -> $GRAPH"

# ④ Catalog: JSSH検索用カタログ分類
jq '
{
  schemas: (map(select(.schema == true)) | map(.file)),
  data: (map(select(.schema == false)) | map(.file))
}
' "$PACK" > "$CATALOG"
echo "[OK] ④ Catalog -> $CATALOG"

# ⑤ Runtime: JSSH実行時のメモリ展開仕様設定
jq -n --slurpfile cat "$CATALOG" '
{
  engine: "JSSH-RUNTIME-V3",
  mode: "STRICT_ZERO_CORE",
  max_memory_mb: 256,
  catalog_summary: $cat[0]
}
' > "$RUNTIME"
echo "[OK] ⑤ Runtime -> $RUNTIME"

# ⑥ Integrity: 完全性検証モデル（SHA256＆サイズチェック）
jq '
{
  algorithm: "sha256",
  assets_count: length,
  total_bytes: (map(.bytes // 0) | add),
  hashes: (map({key: .file, value: .sha256}) | from_entries)
}
' "$PACK" > "$INTEGRITY"
echo "[OK] ⑥ Integrity -> $INTEGRITY"

# ⑦ Bundle: リライト用一括出力バンドル定義
jq -n \
  --slurpfile pack "$PACK" \
  --slurpfile integrity "$INTEGRITY" '
{
  bundle_id: "BUNDLE_30_ZERO_CORE",
  created_at: (now | floor),
  integrity_hash: $integrity[0].total_bytes,
  assets: $pack[0]
}
' > "$BUNDLE"
echo "[OK] ⑦ Bundle -> $BUNDLE"

# ⑧ Master: 解析コア＋運用コアを統合した最上位シングル・ソース・オブ・トゥルース
jq -n \
  --slurpfile manifest "$MANIFEST" \
  --slurpfile registry "$REGISTRY" \
  --slurpfile graph "$GRAPH" \
  --slurpfile runtime "$RUNTIME" \
  --slurpfile integrity "$INTEGRITY" \
  --slurpfile bundle "$BUNDLE" '
{
  master_version: "3.5.0-ZERO-CORE",
  timestamp: (now | floor),
  status: "READY_FOR_JSSH_REWRITE",
  analysis_manifest: $manifest[0],
  registry: $registry[0],
  dependency_graph: $graph[0],
  runtime_config: $runtime[0],
  integrity: $integrity[0],
  bundle: $bundle[0]
}
' > "$MASTER"

echo "=================================================="
echo "[SUCCESS] MASTER CORE BUILT SUCCESSFULLY!"
echo "[TARGET] -> $MASTER"
echo "=================================================="
