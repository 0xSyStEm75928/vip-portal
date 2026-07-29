#!/bin/ash
set -eu

ROOT="${1:-./json_core}"

DATA="$ROOT/ZERO_CORE.data.json"
STORE="$ROOT/ZERO_CORE.storage.json"
INDEX="$ROOT/ZERO_CORE.index.json"
QUERY="$ROOT/ZERO_CORE.query.json"

TIME="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "[*] ZERO_CORE FAST STAGE 10"

jq -n --arg t "$TIME" '
{
 data_version:"1.0.0",
 generated_at:$t,
 schemas:[],
 records:[]
}
' > "$DATA"

jq -n --arg t "$TIME" '
{
 storage_version:"1.0.0",
 generated_at:$t,
 drivers:[
  "json",
  "filesystem",
  "database"
 ],
 mode:"MODULAR"
}
' > "$STORE"

jq -n --arg t "$TIME" '
{
 index_version:"1.0.0",
 generated_at:$t,
 indexes:[],
 searchable:true
}
' > "$INDEX"

jq -n \
 --slurpfile index "$INDEX" \
 --arg t "$TIME" '
{
 query_version:"1.0.0",
 generated_at:$t,
 index:$index[0],
 filters:[]
}
' > "$QUERY"

echo "[SUCCESS] FAST STAGE 10 COMPLETE"
