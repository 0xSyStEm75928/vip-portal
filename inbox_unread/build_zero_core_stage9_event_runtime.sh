#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

EVENT="$ROOT/ZERO_CORE.event.json"
BUS="$ROOT/ZERO_CORE.message_bus.json"
WORKFLOW="$ROOT/ZERO_CORE.workflow.json"
PROCESS="$ROOT/ZERO_CORE.process.json"
LOG="$ROOT/ZERO_CORE.execution_log.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 9"

jq -n --arg t "$TIME" '
{
 event_version:"1.0.0",
 generated_at:$t,
 event_types:[
  "system",
  "user",
  "runtime",
  "audit",
  "workflow"
 ],
 queue:[]
}
' > "$EVENT"

jq -n --arg t "$TIME" '
{
 message_bus_version:"1.0.0",
 generated_at:$t,
 mode:"EVENT_DRIVEN",
 topics:[
  "system",
  "tenant",
  "workflow",
  "audit"
 ],
 status:"READY"
}
' > "$BUS"

jq -n --arg t "$TIME" '
{
 workflow_version:"1.0.0",
 generated_at:$t,
 states:[
  "CREATED",
  "RUNNING",
  "WAITING",
  "COMPLETED",
  "FAILED"
 ],
 transitions:[]
}
' > "$WORKFLOW"

jq -n --arg t "$TIME" '
{
 process_version:"1.0.0",
 generated_at:$t,
 executor:"ZERO_CORE_RUNTIME",
 workers:[],
 status:"IDLE"
}
' > "$PROCESS"

jq -n \
 --slurpfile event "$EVENT" \
 --slurpfile workflow "$WORKFLOW" \
 --arg t "$TIME" '
{
 execution_log_version:"1.0.0",
 generated_at:$t,
 event:$event[0],
 workflow:$workflow[0],
 records:[]
}
' > "$LOG"

echo "[SUCCESS] FAST STAGE 9 COMPLETE"
