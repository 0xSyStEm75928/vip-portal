#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

BOOT="$ROOT/ZERO_CORE.boot.json"
SESSION="$ROOT/ZERO_CORE.session.json"
RUNTIME="$ROOT/ZERO_CORE.runtime_state.json"
POLICY="$ROOT/ZERO_CORE.policy.json"
EVENTS="$ROOT/ZERO_CORE.events.json"
BOOTSTRAP="$ROOT/ZERO_CORE.bootstrap.json"
READY="$ROOT/ZERO_CORE.runtime_ready.json"
SYSTEM="$ROOT/ZERO_CORE.system.json"

echo "[*] ZERO_CORE FAST STAGE 6"

# Boot
jq -n '
{
  boot_version:"1.0.0",
  generated:(now|floor),
  state:"BOOT"
}' > "$BOOT"

# Session
jq -n '
{
  session_version:"1.0.0",
  generated:(now|floor),
  session_id:null
}' > "$SESSION"

# Runtime State
jq -n '
{
  runtime_state_version:"1.0.0",
  generated:(now|floor),
  state:"INITIALIZED"
}' > "$RUNTIME"

# Policy
jq -n '
{
  policy_version:"1.0.0",
  generated:(now|floor),
  mode:"STRICT"
}' > "$POLICY"

# Events
jq -n '
{
  events_version:"1.0.0",
  generated:(now|floor),
  queue:[]
}' > "$EVENTS"

# Bootstrap
jq -n \
  --slurpfile boot "$BOOT" \
  --slurpfile runtime "$RUNTIME" \
  --slurpfile policy "$POLICY" '
{
  bootstrap_version:"1.0.0",
  generated:(now|floor),
  boot:$boot[0],
  runtime:$runtime[0],
  policy:$policy[0]
}' > "$BOOTSTRAP"

# Runtime Ready
jq -n \
  --slurpfile bootstrap "$BOOTSTRAP" '
{
  ready:true,
  generated:(now|floor),
  bootstrap:$bootstrap[0]
}' > "$READY"

# System
jq -n \
  --slurpfile master "$ROOT/ZERO_CORE.master.json" \
  --slurpfile ready "$READY" \
  --slurpfile complete "$ROOT/ZERO_CORE.complete.json" '
{
  system_version:"1.0.0",
  generated:(now|floor),
  master:$master[0],
  runtime:$ready[0],
  complete:$complete[0]
}' > "$SYSTEM"

echo
echo "[SUCCESS] ZERO_CORE FAST STAGE 6 COMPLETE"
echo "[OK] SYSTEM -> $SYSTEM"
