#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

CLI="$ROOT/ZERO_CORE.cli_registry.json"
COMMAND="$ROOT/ZERO_CORE.command_map.json"
INTERFACE="$ROOT/ZERO_CORE.interface_profile.json"
MANIFEST="$ROOT/ZERO_CORE.cli_manifest.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

jq -n \
  --slurpfile cli "$CLI" \
  --slurpfile command "$COMMAND" \
  --slurpfile interface "$INTERFACE" \
  --arg t "$TIME" \
  '{
    cli_manifest_version:"1.0.0",
    generated_at:$t,
    cli:$cli[0],
    commands:$command[0],
    interface:$interface[0],
    state:"CLI_READY"
  }' > "$MANIFEST"

echo "[OK] MANIFEST -> $MANIFEST"
echo "[SUCCESS] STAGE35 PATCH COMPLETE"
