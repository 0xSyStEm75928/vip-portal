#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

BINDING="$ROOT/ZERO_CORE.service_profile_binding.json"
TIERS="$ROOT/ZERO_CORE.business_tier_map.json"
MANIFEST="$ROOT/ZERO_CORE.service_manifest.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE STAGE 47 SERVICE PROFILE BINDING"


# -----------------------------------------------------
# Service Profile Binding
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 service_profile_binding_version:"1.0.0",
 generated_at:$t,

 profiles:{
  personal:{
   tier:"01_PERSONAL",
   mode:"private"
  },

  personal_plus:{
   tier:"02_PERSONAL_PLUS",
   mode:"advanced"
  },

  small_business:{
   tier:"03_SMALL_BUSINESS",
   mode:"organization"
  },

  enterprise:{
   tier:"04_ENTERPRISE",
   mode:"multi_tenant"
  }
 },

 status:"BOUND"
}
' > "$BINDING"


# -----------------------------------------------------
# Business Tier Map
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 business_tier_map_version:"1.0.0",
 generated_at:$t,

 tiers:[
  {
   id:"01_PERSONAL",
   users:"single"
  },
  {
   id:"02_PERSONAL_PLUS",
   users:"individual_operator"
  },
  {
   id:"03_SMALL_BUSINESS",
   users:"organization"
  },
  {
   id:"04_ENTERPRISE",
   users:"multi_tenant"
  }
 ],

 status:"READY"
}
' > "$TIERS"


# -----------------------------------------------------
# Service Manifest
# -----------------------------------------------------

jq -n \
 --slurpfile binding "$BINDING" \
 --slurpfile tiers "$TIERS" \
 --arg t "$TIME" '

{
 service_manifest_version:"1.0.0",
 generated_at:$t,

 binding:$binding[0],
 tiers:$tiers[0],

 state:"SERVICE_READY"
}
' > "$MANIFEST"


echo
echo "[OK] BINDING  -> $BINDING"
echo "[OK] TIERS    -> $TIERS"
echo "[OK] MANIFEST -> $MANIFEST"
echo
echo "[SUCCESS] STAGE 47 BUILD_SUCCESS"
