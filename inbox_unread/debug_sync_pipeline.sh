#!/bin/sh

echo "===== FILE CHECK ====="

ls -l sync_pipeline.py
echo

echo "===== PY_COMPILE ====="
python3 -m py_compile sync_pipeline.py || exit 1
echo

echo "===== RUN ====="
python3 sync_pipeline.py TEST_CUSTOMER_001 OBSERVATION TEST
RET=$?
echo

echo "RETURN CODE=$RET"
echo

echo "===== JSON CHECK ====="
for f in \
json_core/ZERO_CORE.customer.json \
json_core/customer_intake.json \
json_core/customer_lifecycle_gate.json \
json_core/tomorrow_operation_plan.json \
json_core/customer_review_queue.json
do
    printf "%-55s" "$f"
    if [ -f "$f" ]; then
        jq empty "$f" >/dev/null 2>&1 && echo "OK" || echo "INVALID"
    else
        echo "MISSING"
    fi
done

exit $RET
