import subprocess
import sys
from datetime import datetime, timezone


PIPELINE = [
    ("sync_pipeline.py", [
        "TEST_CUSTOMER_001",
        "OBSERVATION",
        "AUTO_RUN"
    ]),

    ("cli_candidate_review.py", []),
    ("cli_business_signal_deep_review.py", []),
    ("customer_deal_sync_check.py", []),
    ("customer_deal_action_plan.py", []),
    ("customer_execution_gate_check.py", []),
    ("customer_final_business_dashboard.py", []),
    ("prioritize_original_targets.py", []),
    ("merge_business_view.py", []),
    ("business_portfolio_status.py", []),
    ("business_execution_queue.py", []),
    ("today_business_focus.py", []),
    ("business_integrity_check.py", []),
    ("business_master_index.py", []),
    ("business_pipeline_summary.py", []),
    ("business_final_report.py", []),
    ("business_release_check.py", [])
]


success = 0
failed = []


print("=" * 72)
print("BUSINESS MASTER RUNNER v3")
print("=" * 72)


for script, args in PIPELINE:

    print("[RUN ]", script)

    try:
        subprocess.run(
            ["python3", script] + args,
            check=True
        )

        print("[ OK ]", script)
        success += 1

    except subprocess.CalledProcessError:
        print("[FAIL]", script)
        failed.append(script)


print("=" * 72)
print("SUMMARY")
print("=" * 72)

print("SUCCESS :", success)
print("FAILED  :", len(failed))

if failed:
    print("FAILED SCRIPTS")
    for f in failed:
        print("-", f)

print("FINISHED:",
      datetime.now(timezone.utc).isoformat())


sys.exit(1 if failed else 0)
