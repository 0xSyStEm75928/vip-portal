import sys
import json
import math

def process_stream_metrics(lines):
    delays = []
    status_counts = {}
    step_counts = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue

        delay = record.get("delay_ms", 0)
        status = record.get("status", "UNKNOWN")
        step = record.get("step", "UNKNOWN")

        delays.append(delay)
        status_counts[status] = status_counts.get(status, 0) + 1
        step_counts[step] = step_counts.get(step, 0) + 1

    if not delays:
        print("No valid data processed.")
        return

    count = len(delays)
    sorted_delays = sorted(delays)
    avg_delay = sum(delays) / count
    min_delay = sorted_delays[0]
    max_delay = sorted_delays[-1]

    # パーセンタイル計算 (標準ライブラリのみで実装)
    def percentile(arr, p):
        k = (len(arr) - 1) * (p / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return arr[int(k)]
        d0 = arr[int(f)] * (c - k)
        d1 = arr[int(c)] * (k - f)
        return d0 + d1

    p95_delay = percentile(sorted_delays, 95)
    p99_delay = percentile(sorted_delays, 99)

    summary = {
        "metrics_summary": {
            "total_records": count,
            "latency_ms": {
                "avg": round(avg_delay, 2),
                "min": min_delay,
                "max": max_delay,
                "p95": round(p95_delay, 2),
                "p99": round(p99_delay, 2)
            },
            "status_distribution": status_counts,
            "step_distribution": step_counts
        }
    }

    print(json.dumps(summary, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    process_stream_metrics(lines)
