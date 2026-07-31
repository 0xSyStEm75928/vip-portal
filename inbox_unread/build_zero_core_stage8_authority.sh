#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

IDENTITY="$ROOT/ZERO_CORE.identity.json"
ROLE="$ROOT/ZERO_CORE.role.json"
PERMISSION="$ROOT/ZERO_CORE.permission.json"
POLICY="$ROOT/ZERO_CORE.policy_engine.json"
AUDIT="$ROOT/ZERO_CORE.audit_chain.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 8: AUTHORITY ENGINE"

jq -n --arg time "$TIME" '
{
  identity_version:"1.0.0",
  generated_at:$time,
  identity_provider:"ZERO_CORE_NATIVE",
  subjects:[],
  status:"ACTIVE"
}
' > "$IDENTITY"


jq -n --arg time "$TIME" '
{
  role_version:"1.0.0",
  generated_at:$time,
  hierarchy:[
    "super_admin",
    "tenant_admin",
    "manager",
    "staff",
    "external_auditor",
    "viewer"
  ]
}
' > "$ROLE"


jq -n --arg time "$TIME" '
{
  permission_version:"1.0.0",
  generated_at:$time,
  permissions:[
    "read",
    "write",
    "execute",
    "admin",
    "audit",
    "manage"
  ],
  namespace_control:true
}
' > "$PERMISSION"


jq -n \
 --slurpfile role "$ROLE" \
 --slurpfile permission "$PERMISSION" \
 --arg time "$TIME" '

{
  policy_engine_version:"1.0.0",
  generated_at:$time,
  enforcement:"STRICT",
  default:"DENY",
  role_registry:$role[0],
  permission_registry:$permission[0]
}
' > "$POLICY"


jq -n \
 --slurpfile identity "$IDENTITY" \
 --slurpfile policy "$POLICY" \
 --arg time "$TIME" '

{
  audit_chain_version:"1.0.0",
  generated_at:$time,
  immutable:true,
  identity:$identity[0],
  policy:$policy[0],
  events:[]
}
' > "$AUDIT"


echo
echo "[OK] IDENTITY  -> $IDENTITY"
echo "[OK] ROLE      -> $ROLE"
echo "[OK] PERMISSION-> $PERMISSION"
echo "[OK] POLICY    -> $POLICY"
echo "[OK] AUDIT    -> $AUDIT"
echo
echo "[SUCCESS] FAST STAGE 8 COMPLETE"
