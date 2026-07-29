#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

NODE="$ROOT/ZERO_CORE.node_registry.json"
SYNC="$ROOT/ZERO_CORE.sync.json"
FEDERATION="$ROOT/ZERO_CORE.federation.json"
CLUSTER="$ROOT/ZERO_CORE.cluster_state.json"
HEALTH="$ROOT/ZERO_CORE.node_health.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 22 FEDERATION LAYER"


# -----------------------------------------------------
# Node Registry
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 node_registry_version:"1.0.0",
 generated_at:$t,

 node_type:[
  "primary",
  "secondary",
  "federated"
 ],

 nodes:[],
 status:"READY"
}
' > "$NODE"


# -----------------------------------------------------
# Sync Engine
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 sync_version:"1.0.0",
 generated_at:$t,

 mode:"CONTROLLED_SYNC",

 sync_targets:[
  "runtime",
  "registry",
  "policy",
  "state"
 ],

 queue:[]
}
' > "$SYNC"


# -----------------------------------------------------
# Federation
# -----------------------------------------------------

jq -n \
 --slurpfile node "$NODE" \
 --slurpfile sync "$SYNC" \
 --arg t "$TIME" '

{
 federation_version:"1.0.0",
 generated_at:$t,

 node_registry:$node[0],
 sync_engine:$sync[0],

 federation_mode:"MULTI_NODE",

 members:[]
}
' > "$FEDERATION"


# -----------------------------------------------------
# Cluster State
# -----------------------------------------------------

jq -n \
 --slurpfile federation "$FEDERATION" \
 --arg t "$TIME" '

{
 cluster_state_version:"1.0.0",
 generated_at:$t,

 federation:$federation[0],

 topology:"READY",

 state:"STABLE"
}
' > "$CLUSTER"


# -----------------------------------------------------
# Node Health
# -----------------------------------------------------

jq -n \
 --slurpfile cluster "$CLUSTER" \
 --arg t "$TIME" '

{
 node_health_version:"1.0.0",
 generated_at:$t,

 cluster:$cluster[0],

 checks:[
  "connectivity",
  "sync",
  "integrity"
 ],

 status:"HEALTHY"
}
' > "$HEALTH"


echo
echo "[OK] NODE       -> $NODE"
echo "[OK] SYNC       -> $SYNC"
echo "[OK] FEDERATION -> $FEDERATION"
echo "[OK] CLUSTER    -> $CLUSTER"
echo "[OK] HEALTH     -> $HEALTH"
echo
echo "[SUCCESS] FAST STAGE 22 BUILD_SUCCESS"
