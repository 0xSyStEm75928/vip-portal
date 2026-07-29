#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

TENANT="$ROOT/ZERO_CORE.tenant.json"
ORG="$ROOT/ZERO_CORE.organization.json"
NAMESPACE="$ROOT/ZERO_CORE.namespace.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 14"

jq -n --arg t "$TIME" '
{
 tenant_version:"1.0.0",
 generated_at:$t,
 multi_tenant:true,
 tenants:[]
}
' > "$TENANT"

jq -n --arg t "$TIME" '
{
 organization_version:"1.0.0",
 generated_at:$t,
 organizations:[],
 hierarchy:[
  "company",
  "department",
  "team"
 ]
}
' > "$ORG"

jq -n --arg t "$TIME" '
{
 namespace_version:"1.0.0",
 generated_at:$t,
 isolation:true,
 namespaces:[]
}
' > "$NAMESPACE"

echo "[SUCCESS] FAST STAGE 14 COMPLETE"
