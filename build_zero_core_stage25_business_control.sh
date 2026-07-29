#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

LICENSE="$ROOT/ZERO_CORE.license.json"
PLAN="$ROOT/ZERO_CORE.plan.json"
BILLING="$ROOT/ZERO_CORE.billing.json"
CUSTOMER="$ROOT/ZERO_CORE.customer.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 25 BUSINESS CONTROL"

jq -n --arg t "$TIME" '
{
 license_version:"1.0.0",
 generated_at:$t,
 licenses:[],
 validation:"REQUIRED"
}
' > "$LICENSE"

jq -n --arg t "$TIME" '
{
 plan_version:"1.0.0",
 generated_at:$t,
 tiers:[
  "personal",
  "personal_plus",
  "small_business",
  "enterprise"
 ]
}
' > "$PLAN"

jq -n --arg t "$TIME" '
{
 billing_version:"1.0.0",
 generated_at:$t,
 invoices:[],
 status:"READY"
}
' > "$BILLING"

jq -n --arg t "$TIME" '
{
 customer_version:"1.0.0",
 generated_at:$t,
 customers:[]
}
' > "$CUSTOMER"

echo "[SUCCESS] FAST STAGE 25 BUILD_SUCCESS"
