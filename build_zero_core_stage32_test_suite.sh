#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

TEST="$ROOT/ZERO_CORE.test_suite.json"
REGRESSION="$ROOT/ZERO_CORE.regression.json"
CI="$ROOT/ZERO_CORE.ci_prepare.json"
REPORT="$ROOT/ZERO_CORE.test_report.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 32 TEST / REGRESSION / CI"


# -----------------------------------------------------
# Test Suite
# -----------------------------------------------------

jq -n --arg t "$TIME" '
{
 test_suite_version:"1.0.0",
 generated_at:$t,

 suites:[
  "schema",
  "runtime",
  "authority",
  "security",
  "recovery",
  "release"
 ],

 status:"READY"
}
' > "$TEST"


# -----------------------------------------------------
# Regression Check
# -----------------------------------------------------

jq -n \
 --slurpfile test "$TEST" \
 --arg t "$TIME" '

{
 regression_version:"1.0.0",
 generated_at:$t,

 test_suite:$test[0],

 checks:[
  "compatibility",
  "integrity",
  "dependency"
 ],

 result:"PENDING"
}
' > "$REGRESSION"


# -----------------------------------------------------
# CI Preparation
# -----------------------------------------------------

jq -n --arg t "$TIME" '

{
 ci_prepare_version:"1.0.0",
 generated_at:$t,

 pipeline:[
  "validate",
  "test",
  "audit",
  "release"
 ],

 environment:[
  "local",
  "server"
 ],

 status:"READY"
}
' > "$CI"


# -----------------------------------------------------
# Test Report
# -----------------------------------------------------

jq -n \
 --slurpfile test "$TEST" \
 --slurpfile regression "$REGRESSION" \
 --slurpfile ci "$CI" \
 --arg t "$TIME" '

{
 test_report_version:"1.0.0",
 generated_at:$t,

 test_suite:$test[0],
 regression:$regression[0],
 ci_prepare:$ci[0],

 status:"TEST_FRAME_READY"
}
' > "$REPORT"


echo
echo "[OK] TEST       -> $TEST"
echo "[OK] REGRESSION -> $REGRESSION"
echo "[OK] CI         -> $CI"
echo "[OK] REPORT     -> $REPORT"
echo
echo "[SUCCESS] FAST STAGE 32 BUILD_SUCCESS"
