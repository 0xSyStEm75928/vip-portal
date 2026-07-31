import subprocess, re
from collections import Counter

def analyze_history_anatomy():
    # シェル履歴を取得（.bash_history または current session）
    try:
        res = subprocess.run("history | tail -n 100", shell=True, capture_output=True, text=True, executable='/bin/bash')
        lines = res.stdout.strip().split('\n')
    except Exception:
        lines = []

    print("="*65)
    print("      【 COMMAND ANATOMY : 無駄コマンド＆重複解剖レポート 】")
    print("="*65)

    raw_cmds = []
    for line in lines:
        # 行番号を取り除き、純粋なコマンド文字列を抽出
        parts = re.split(r'\s+', line.strip(), maxsplit=1)
        if len(parts) > 1:
            raw_cmds.append(parts[1].strip())

    total_count = len(raw_cmds)
    if total_count == 0:
        print("[INFO] 履歴が空か、取得できませんでした。テスト用サンプルを解剖します。")
        raw_cmds = [
            "python3 sync_pipeline.py CUSTOMER_001 10",
            "python3 sync_pipeline.py CUSTOMER_001 50",
            "python3 sync_pipeline.py CUSTOMER_001 100",
            "jq . json_core/dispatch_next_action_queue.json",
            "jq . json_core/dispatch_next_action_queue.json", # 重複
            "python3 sync_pipeline.py CUSTOMER_001 100",     # 重複・DAG導入により無駄化
            "ls -la",
            "dhist CUSTOMER_001 N1_INGRESS"
        ]
        total_count = len(raw_cmds)

    # 重複・冗長コマンドのカウント
    counts = Counter(raw_cmds)
    duplicates = {cmd: cnt for cmd, cnt in counts.items() if cnt > 1}
    
    # 旧式パイプラインコマンド（dhist導入により無駄化したもの）の検出
    legacy_cmds = [cmd for cmd in raw_cmds if "sync_pipeline.py" in cmd]

    redundant_count = sum(cnt - 1 for cnt in duplicates.values()) + len(legacy_cmds)
    waste_rate = round((redundant_count / total_count) * 100, 1) if total_count > 0 else 0

    print(f"■ 総分析コマンド数   : {total_count} 件")
    print(f"■ 無駄・冗長コマンド  : {redundant_count} 件 (無駄率: {waste_rate}%)")
    print("-" * 65)
    print("【1. 解剖された「重複・連鎖連打」コマンド (Duplicated Anatomy)】")
    if duplicates:
        for cmd, cnt in duplicates.items():
            print(f"  [連打 {cnt}回] {cmd}")
    else:
        print("  (なし - クリーンな状態です)")

    print("-" * 65)
    print("【2. DAG化(`dhist`)によって統合・無駄化した旧式コマンド】")
    if legacy_cmds:
        for cmd in set(legacy_cmds):
            print(f"  [代替推奨] {cmd}  ==>  dhist を使えば1発で全自動連動")
    else:
        print("  (なし)")

    print("="*65)
    print(f">>> ANATOMY SUMMARY: 履歴の {100 - waste_rate}% が最適化された有効コマンドです <<<")
    print("="*65)

if __name__ == "__main__":
    analyze_history_anatomy()
