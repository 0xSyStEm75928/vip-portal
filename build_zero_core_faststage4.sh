#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

SIGNATURE="$ROOT/ZERO_CORE.signature.json"
INVENTORY="$ROOT/ZERO_CORE.inventory.json"
PACKAGE="$ROOT/ZERO_CORE.package.json"
ARCHIVE="$ROOT/ZERO_CORE.archive.json"
STATE="$ROOT/ZERO_CORE.state.json"
CHECKPOINT="$ROOT/ZERO_CORE.checkpoint.json"
READY="$ROOT/ZERO_CORE.ready.json"
DIST="$ROOT/ZERO_CORE.dist.json"

echo "[*] ZERO_CORE FAST STAGE 4"

# Signature
jq -n \
  --slurpfile master "$ROOT/ZERO_CORE.master.json" '
{
  signature_version:"1.0.0",
  generated:(now|floor),
  algorithm:"SHA-256",
  master:$master[0]
}' > "$SIGNATURE"

# Inventory
jq -n \
  --slurpfile manifest "$ROOT/ZERO_CORE.30manifest.json" \
  --slurpfile catalog "$ROOT/ZERO_CORE.catalog.json" '
{
  inventory_version:"1.0.0",
  generated:(now|floor),
  manifest:$manifest[0],
  catalog:$catalog[0]
}' > "$INVENTORY"

# Package
jq -n \
  --slurpfile master "$ROOT/ZERO_CORE.master.json" \
  --slurpfile bundle "$ROOT/ZERO_CORE.bundle.json" '
{
  package_version:"1.0.0",
  generated:(now|floor),
  master:$master[0],
  bundle:$bundle[0]
}' > "$PACKAGE"

# Archive
jq -n \
  --slurpfile package "$PACKAGE" '
{
  archive_version:"1.0.0",
  generated:(now|floor),
  package:$package[0]
}' > "$ARCHIVE"

# State
jq -n '
{
  state:"READY",
  generated:(now|floor)
}' > "$STATE"

# Checkpoint
jq -n \
  --slurpfile state "$STATE" \
  --slurpfile archive "$ARCHIVE" '
{
  checkpoint_version:"1.0.0",
  generated:(now|floor),
  state:$state[0],
  archive:$archive[0]
}' > "$CHECKPOINT"

# Ready
jq -n \
  --slurpfile checkpoint "$CHECKPOINT" '
{
  ready:true,
  generated:(now|floor),
  checkpoint:$checkpoint[0]
}' > "$READY"

# Dist
jq -n \
  --slurpfile ready "$READY" \
  --slurpfile package "$PACKAGE" '
{
  dist_version:"1.0.0",
  generated:(now|floor),
  ready:$ready[0],
  package:$package[0]
}' > "$DIST"

echo "[SUCCESS] FAST STAGE 4 COMPLETE"
