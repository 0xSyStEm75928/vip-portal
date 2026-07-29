#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

AUDIT="$ROOT/ZERO_CORE.audit.json"
DEPENDENCY="$ROOT/ZERO_CORE.dependency.json"
PIPELINE="$ROOT/ZERO_CORE.pipeline.json"
RELEASE="$ROOT/ZERO_CORE.release.json"
EXPORT="$ROOT/ZERO_CORE.export.json"
SNAPSHOT="$ROOT/ZERO_CORE.snapshot.json"
SUMMARY="$ROOT/ZERO_CORE.summary.json"
FINAL="$ROOT/ZERO_CORE.final.json"

echo "[*] ZERO_CORE FAST STAGE 3"

# ----------------------------------------------------------
# Audit
# ----------------------------------------------------------
jq -n \
  --slurpfile master "$ROOT/ZERO_CORE.master.json" \
  --slurpfile integrity "$ROOT/ZERO_CORE.integrity.json" '
{
  audit_version:"1.0.0",
  generated:(now|floor),
  master:$master[0],
  integrity:$integrity[0]
}' > "$AUDIT"

# ----------------------------------------------------------
# Dependency
# ----------------------------------------------------------
jq -n \
  --slurpfile graph "$ROOT/ZERO_CORE.graph.json" '
{
  dependency_version:"1.0.0",
  generated:(now|floor),
  graph:$graph[0]
}' > "$DEPENDENCY"

# ----------------------------------------------------------
# Pipeline
# ----------------------------------------------------------
jq -n \
  --slurpfile runtime "$ROOT/ZERO_CORE.runtime.json" \
  --slurpfile registry "$ROOT/ZERO_CORE.registry.json" '
{
  pipeline_version:"1.0.0",
  generated:(now|floor),
  runtime:$runtime[0],
  registry:$registry[0]
}' > "$PIPELINE"

# ----------------------------------------------------------
# Release
# ----------------------------------------------------------
jq -n \
  --slurpfile bundle "$ROOT/ZERO_CORE.bundle.json" '
{
  release_version:"1.0.0",
  generated:(now|floor),
  bundle:$bundle[0]
}' > "$RELEASE"

# ----------------------------------------------------------
# Export
# ----------------------------------------------------------
jq -n \
  --slurpfile release "$RELEASE" \
  --slurpfile master "$ROOT/ZERO_CORE.master.json" '
{
  export_version:"1.0.0",
  generated:(now|floor),
  release:$release[0],
  master:$master[0]
}' > "$EXPORT"

# ----------------------------------------------------------
# Snapshot
# ----------------------------------------------------------
jq -n \
  --slurpfile master "$ROOT/ZERO_CORE.master.json" '
{
  snapshot_version:"1.0.0",
  generated:(now|floor),
  master:$master[0]
}' > "$SNAPSHOT"

# ----------------------------------------------------------
# Summary
# ----------------------------------------------------------
jq -n \
  --slurpfile metrics "$ROOT/ZERO_CORE.metrics.json" \
  --slurpfile audit "$AUDIT" '
{
  summary_version:"1.0.0",
  generated:(now|floor),
  metrics:$metrics[0],
  audit:$audit[0]
}' > "$SUMMARY"

# ----------------------------------------------------------
# Final
# ----------------------------------------------------------
jq -n \
  --slurpfile master "$ROOT/ZERO_CORE.master.json" \
  --slurpfile summary "$SUMMARY" \
  --slurpfile export "$EXPORT" '
{
  zero_core_version:"1.0.0",
  generated:(now|floor),
  status:"READY",
  master:$master[0],
  summary:$summary[0],
  export:$export[0]
}' > "$FINAL"

echo "[OK] AUDIT      -> $AUDIT"
echo "[OK] DEPENDENCY -> $DEPENDENCY"
echo "[OK] PIPELINE   -> $PIPELINE"
echo "[OK] RELEASE    -> $RELEASE"
echo "[OK] EXPORT     -> $EXPORT"
echo "[OK] SNAPSHOT   -> $SNAPSHOT"
echo "[OK] SUMMARY    -> $SUMMARY"
echo "[OK] FINAL      -> $FINAL"

echo
echo "[SUCCESS] ZERO_CORE FAST STAGE 3 COMPLETE"
