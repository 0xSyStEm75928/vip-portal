#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

API="$ROOT/ZERO_CORE.api_gateway.json"
SERVICE="$ROOT/ZERO_CORE.service_registry.json"
LIMIT="$ROOT/ZERO_CORE.rate_policy.json"
ROUTE="$ROOT/ZERO_CORE.route.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 24 SERVICE GATEWAY"

jq -n --arg t "$TIME" '
{
 api_gateway_version:"1.0.0",
 generated_at:$t,
 mode:"CONTROLLED",
 routes:[]
}
' > "$API"

jq -n --arg t "$TIME" '
{
 service_registry_version:"1.0.0",
 generated_at:$t,
 services:[]
}
' > "$SERVICE"

jq -n --arg t "$TIME" '
{
 rate_policy_version:"1.0.0",
 generated_at:$t,
 limits:[],
 enforcement:"ACTIVE"
}
' > "$LIMIT"

jq -n \
 --slurpfile api "$API" \
 --slurpfile service "$SERVICE" \
 --arg t "$TIME" '
{
 route_version:"1.0.0",
 generated_at:$t,
 gateway:$api[0],
 services:$service[0]
}
' > "$ROUTE"

echo "[SUCCESS] FAST STAGE 24 BUILD_SUCCESS"
