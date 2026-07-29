#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

LIFECYCLE="$ROOT/ZERO_CORE.lifecycle.json"
RECOVERY="$ROOT/ZERO_CORE.recovery.json"
DEPLOY="$ROOT/ZERO_CORE.deploy.json"
CHANNELS="$ROOT/ZERO_CORE.channels.json"
DISTRIBUTION="$ROOT/ZERO_CORE.distribution.json"
CHANGELOG="$ROOT/ZERO_CORE.changelog.json"
REPORT="$ROOT/ZERO_CORE.report.json"
COMPLETE="$ROOT/ZERO_CORE.complete.json"

echo "[*] ZERO_CORE FAST STAGE 5"

# ----------------------------------------------------------
# Lifecycle
# ----------------------------------------------------------
jq -n '
{
  lifecycle_version:"1.0.0",
  generated:(now|floor),
  phase:"COMPLETE",
  state:"ACTIVE"
}' > "$LIFECYCLE"

# ----------------------------------------------------------
# Recovery
# ----------------------------------------------------------
jq -n \
  --slurpfile master "$ROOT/ZERO_CORE.master.json" '
{
  recovery_version:"1.0.0",
  generated:(now|floor),
  source:$master[0]
}' > "$RECOVERY"

# ----------------------------------------------------------
# Deploy
# ----------------------------------------------------------
jq -n \
  --slurpfile dist "$ROOT/ZERO_CORE.dist.json" '
{
  deploy_version:"1.0.0",
  generated:(now|floor),
  distribution:$dist[0]
}' > "$DEPLOY"

# ----------------------------------------------------------
# Channels
# ----------------------------------------------------------
jq -n '
{
  channels_version:"1.0.0",
  generated:(now|floor),
  channels:[
    "runtime",
    "archive",
    "bundle",
    "master"
  ]
}' > "$CHANNELS"

# ----------------------------------------------------------
# Distribution
# ----------------------------------------------------------
jq -n \
  --slurpfile deploy "$DEPLOY" \
  --slurpfile channels "$CHANNELS" '
{
  distribution_version:"1.0.0",
  generated:(now|floor),
  deploy:$deploy[0],
  channels:$channels[0]
}' > "$DISTRIBUTION"

# ----------------------------------------------------------
# Changelog
# ----------------------------------------------------------
jq -n '
{
  changelog_version:"1.0.0",
  generated:(now|floor),
  entries:[]
}' > "$CHANGELOG"

# ----------------------------------------------------------
# Report
# ----------------------------------------------------------
jq -n \
  --slurpfile summary "$ROOT/ZERO_CORE.summary.json" \
  --slurpfile distribution "$DISTRIBUTION" '
{
  report_version:"1.0.0",
  generated:(now|floor),
  summary:$summary[0],
  distribution:$distribution[0]
}' > "$REPORT"

# ----------------------------------------------------------
# Complete
# ----------------------------------------------------------
jq -n \
  --slurpfile master "$ROOT/ZERO_CORE.master.json" \
  --slurpfile report "$REPORT" \
  --slurpfile lifecycle "$LIFECYCLE" '
{
  zero_core_version:"1.0.0",
  generated:(now|floor),
  status:"COMPLETE",
  master:$master[0],
  report:$report[0],
  lifecycle:$lifecycle[0]
}' > "$COMPLETE"

echo
echo "[SUCCESS] ZERO_CORE FAST STAGE 5 COMPLETE"
echo "[OK] COMPLETE -> $COMPLETE"
