#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

GRAPH="$ROOT/ZERO_CORE.graph.json"
METRICS="$ROOT/ZERO_CORE.metrics.json"
RUNTIME="$ROOT/ZERO_CORE.runtime.json"
MASTER="$ROOT/ZERO_CORE.master.json"
CATALOG="$ROOT/ZERO_CORE.catalog.json"
REGISTRY="$ROOT/ZERO_CORE.registry.json"
INTEGRITY="$ROOT/ZERO_CORE.integrity.json"
BUNDLE="$ROOT/ZERO_CORE.bundle.json"

echo "[*] ZERO_CORE FAST STAGE 2"

# ------------------------------------------------------------------
# Graph
# ------------------------------------------------------------------
jq '.graph' \
"$ROOT/ZERO_CORE.graph_map.json" \
> "$GRAPH"

# ------------------------------------------------------------------
# Metrics
# ------------------------------------------------------------------
jq '
{
  files:.total_files,
  bytes:.total_bytes,
  lines:.total_lines,
  schemas:.schema_files,
  json:.json_files
}
' \
"$ROOT/ZERO_CORE.30meta.json" \
> "$METRICS"

# ------------------------------------------------------------------
# Catalog
# ------------------------------------------------------------------
jq '
.assets
| map({
    file,
    sha256,
    bytes,
    lines
})
' \
"$ROOT/ZERO_CORE.30meta.json" \
> "$CATALOG"

# ------------------------------------------------------------------
# Registry
# ------------------------------------------------------------------
jq -n \
 --slurpfile catalog "$CATALOG" \
 '{
    registry_version:"1.0.0",
    generated:(now|floor),
    catalog:$catalog[0]
 }' \
> "$REGISTRY"

# ------------------------------------------------------------------
# Integrity
# ------------------------------------------------------------------
jq -n \
 --slurpfile hashes "$ROOT/ZERO_CORE.30hashmap.json" \
 '{
    algorithm:"SHA-256",
    generated:(now|floor),
    hashes:$hashes[0]
 }' \
> "$INTEGRITY"

# ------------------------------------------------------------------
# Runtime
# ------------------------------------------------------------------
jq -n \
 --slurpfile graph "$GRAPH" \
 --slurpfile metrics "$METRICS" \
 '{
    runtime_version:"1.0.0",
    generated:(now|floor),
    graph:$graph[0],
    metrics:$metrics[0]
 }' \
> "$RUNTIME"

# ------------------------------------------------------------------
# Bundle
# ------------------------------------------------------------------
jq -n \
 --slurpfile runtime "$RUNTIME" \
 --slurpfile registry "$REGISTRY" \
 --slurpfile integrity "$INTEGRITY" \
 '{
    bundle_version:"1.0.0",
    runtime:$runtime[0],
    registry:$registry[0],
    integrity:$integrity[0]
 }' \
> "$BUNDLE"

# ------------------------------------------------------------------
# Master
# ------------------------------------------------------------------
jq -n \
 --slurpfile manifest "$ROOT/ZERO_CORE.30manifest.json" \
 --slurpfile bundle "$BUNDLE" \
 '{
    master_version:"1.0.0",
    generated:(now|floor),
    manifest:$manifest[0],
    bundle:$bundle[0]
 }' \
> "$MASTER"

echo
echo "[OK] GRAPH      -> $GRAPH"
echo "[OK] METRICS    -> $METRICS"
echo "[OK] CATALOG    -> $CATALOG"
echo "[OK] REGISTRY   -> $REGISTRY"
echo "[OK] INTEGRITY  -> $INTEGRITY"
echo "[OK] RUNTIME    -> $RUNTIME"
echo "[OK] BUNDLE     -> $BUNDLE"
echo "[OK] MASTER     -> $MASTER"
echo
echo "[SUCCESS] ZERO_CORE FAST STAGE 2 COMPLETE"
