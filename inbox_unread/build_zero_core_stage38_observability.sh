#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

OBS="$ROOT/ZERO_CORE.observability.json"
METRICS="$ROOT/ZERO_CORE.metrics_runtime.json"
HEALTH="$ROOT/ZERO_CORE.health_monitor.json"
MANIFEST="$ROOT/ZERO_CORE.observability_manifest.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 38 OBSERVABILITY"


# -----------------------------------------------------
# Observability Registry
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 observability_version:"1.0.0",
 generated_at:$t,

 layers:[
  "runtime",
  "performance",
  "security",
  "audit"
 ],

 status:"READY"
}
' > "$OBS"


# -----------------------------------------------------
# Runtime Metrics
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 metrics_runtime_version:"1.0.0",
 generated_at:$t,

 metrics:[
  "execution_count",
  "runtime_state",
  "error_count",
  "audit_count"
 ],

 collection:"ENABLED"
}
' > "$METRICS"


# -----------------------------------------------------
# Health Monitor
# -----------------------------------------------------

jq -n \
 --slurpfile metrics "$METRICS" \
 --arg t "$TIME" '

{
 health_monitor_version:"1.0.0",
 generated_at:$t,

 metrics:$metrics[0],

 checks:[
  "runtime",
  "integrity",
  "availability"
 ],

 status:"HEALTHY"
}
' > "$HEALTH"


# -----------------------------------------------------
# Manifest
# -----------------------------------------------------

jq -n \
 --slurpfile obs "$OBS" \
 --slurpfile health "$HEALTH" \
 --arg t "$TIME" '

{
 observability_manifest_version:"1.0.0",
 generated_at:$t,

 observability:$obs[0],
 health:$health[0],

 state:"MONITORING_READY"
}
' > "$MANIFEST"


echo
echo "[OK] OBSERVABILITY -> $OBS"
echo "[OK] METRICS       -> $METRICS"
echo "[OK] HEALTH        -> $HEALTH"
echo "[OK] MANIFEST      -> $MANIFEST"
echo
echo "[SUCCESS] FAST STAGE 38 BUILD_SUCCESS"
