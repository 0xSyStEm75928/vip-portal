import subprocess
import sys

PIPELINE = [
    "sync_pipeline.py",
    "cli_candidate_review.py",
    "cli_business_signal_deep_review.py",
    "customer_deal_sync_check.py",
    "customer_deal_action_plan.py",
    "customer_execution_gate_check.py",
    "customer_final_business_dashboard.py",
    "prioritize_original_targets.py",
    "merge_business_view.py",
    "business_portfolio_status.py",
    "business_execution_queue.py",
    "today_business_focus.py",
    "business_integrity_check.py",
    "business_master_index.py",
    "business_pipeline_summary.py"
]

success = []
failed = []

print("=" * 72)
print("BUSINESS PIPELINE RUNNER")
print("=" * 72)

for script in PIPELINE:

    print(f"[RUN ] {script}")

    proc = subprocess.run(
        ["python3", script],
        capture_output=True,
        text=True
    )

    if proc.returncode == 0:
        success.append(script)
        print(f"[ OK ] {script}")
    else:
        failed.append(script)
        print(f"[FAIL] {script}")
        if proc.stderr:
            print(proc.stderr.strip())

print("=" * 72)
print("SUMMARY")
print("=" * 72)
print("SUCCESS :", len(success))
print("FAILED  :", len(failed))

if failed:
    print("\nFAILED SCRIPTS")
    for s in failed:
        print("-", s)
    sys.exit(1)

print("\nPIPELINE STATUS : HEALTHY")
