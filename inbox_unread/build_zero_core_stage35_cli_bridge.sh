
#!/bin/ash

set -eu

ROOT="${1:-./json_core}"

CLI="$ROOT/ZERO_CORE.cli_registry.json"

COMMAND="$ROOT/ZERO_CORE.command_map.json"

INTERFACE="$ROOT/ZERO_CORE.interface_profile.json"

MANIFEST="$ROOT/ZERO_CORE.cli_manifest.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 35 CLI / INTERFACE BRIDGE"

# -----------------------------------------------------

# CLI Registry

# -----------------------------------------------------

jq -n --arg t "$TIME" '

{

 cli_registry_version:"1.0.0",

 generated_at:$t,

 command_entry:"sun",

 commands:[

  "status",

  "health",

  "audit",

  "profile",

  "runtime",

  "export"

 ],

 status:"READY"

}

' > "$CLI"

# -----------------------------------------------------

# Command Map

# -----------------------------------------------------

jq -n --arg t "$TIME" '

{

 command_map_version:"1.0.0",

 generated_at:$t,

 mappings:{

  "sun status":"system status",

  "sun health":"health check",

  "sun audit":"audit report",

  "sun profile":"profile manager",

  "sun runtime":"runtime control",

  "sun export":"artifact export"

 }

}

' > "$COMMAND"

# -----------------------------------------------------

# Interface Profile

# -----------------------------------------------------

jq -n --arg t "$TIME" '

{

 interface_profile_version:"1.0.0",

 generated_at:$t,

 mode:[

  "cui",

  "cli",

  "json"

 ],

 design:[

  "pipeable",

  "scriptable",

  "automation_ready"

 ],

 status:"READY"

}

' > "$INTERFACE"

# -----------------------------------------------------

# CLI Manifest

# -----------------------------------------------------

jq -n \

 --slurpfile cli "$CLI" \

 --slurpfile command "$COMMAND" \

 --slurpfile interface "$INTERFACE" \

 --arg t "$TIME" '

{

 cli_manifest_version:"1.0.0",

 generated_at:$t,

 cli:$cli[0],

 commands:$command[0],

 interface:$interface[0],

 state:"CLI_READY"

}

' > "$MANIFEST"

echo

echo "[OK] CLI        -> $CLI"

echo "[OK] COMMAND    -> $COMMAND"

echo "[OK] INTERFACE  -> $INTERFACE"

echo "[OK] MANIFEST   -> $MANIFEST"

echo

echo "[SUCCESS] FAST STAGE 35 BUILD_SUCCESS"

