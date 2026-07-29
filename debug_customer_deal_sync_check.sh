#!/bin/sh

echo "===== CUSTOMER DEAL SYNC DEBUG ====="

echo
echo "===== FILE CHECK ====="

ls -l customer_deal_sync_check.py

echo
echo "===== PY COMPILE ====="

python3 -m py_compile customer_deal_sync_check.py

if [ $? -ne 0 ]; then
    echo "PY_COMPILE FAILED"
    exit 1
fi


echo
echo "===== JSON DEPENDENCY CHECK ====="

for f in \
json_core/customer_real_deal_review.json \
json_core/customer_deal_sync_result.json \
json_core/customer_deal_action_plan.json \
json_core/ZERO_CORE.customer.json

do

    if [ -f "$f" ]; then
        jq empty "$f" && echo "$f OK"
    else
        echo "$f MISSING"
    fi

done


echo
echo "===== DIRECT RUN ====="

python3 customer_deal_sync_check.py

echo
echo "RETURN CODE=$?"

echo
echo "===== DEBUG END ====="
