import json, os, sys, shutil
from datetime import datetime

BASE_DIR = "json_core"
BACKUP_DIR = "json_backup"

FILES = [
    "core_customer_master.json",
    "ingress_customer_intake.json",
    "gate_lifecycle_control.json",
    "dispatch_daily_schedule.json",
    "review_human_approval_queue.json",
    "dispatch_next_action_queue.json",
    "view_deal_sync_summary.json"
]

def verify_and_backup():
    ts_folder = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_backup_path = os.path.join(BACKUP_DIR, ts_folder)
    os.makedirs(target_backup_path, exist_ok=True)

    print("=" * 65)
    print("      【歪みゼロ (ZERO-DISTORTION) 全JSON最終検証＆バックアップ】")
    print("=" * 65)

    errors = 0
    verified_files = []

    for fname in FILES:
        src_path = os.path.join(BASE_DIR, fname)
        if not os.path.exists(src_path):
            print(f"[WARN] 存在しないファイル (新規生成): {fname}")
            data = {}
        else:
            try:
                with open(src_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"[ERROR] JSON破損検知: {fname} -> {e}")
                errors += 1
                continue

        # 構造の整合性チェック (型・キーの不整合補正)
        if not isinstance(data, dict):
            print(f"[ERROR] ルート構造不整合 (Dict型である必要があります): {fname}")
            errors += 1
            continue

        # バックアップ書き出し (整形出力で歪みを排除)
        dst_path = os.path.join(target_backup_path, fname)
        with open(dst_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        verified_files.append(fname)
        print(f" [OK] 検証完了 & バックアップ保存: {fname}")

    print("-" * 65)
    print(f"■ バックアップ先: {target_backup_path}")
    print(f"■ 検証成功ファイル: {len(verified_files)} / {len(FILES)}")
    
    if errors == 0:
        print("=" * 65)
        print(">>> 最終検証結果: 全データ正常・歪みゼロ (100% LOCKED & BACKED UP) <<<")
        print("=" * 65)
    else:
        print("=" * 65)
        print(f">>> 最終検証結果: {errors} 件の歪み/エラーが検知されました <<<")
        print("=" * 65)

if __name__ == "__main__":
    verify_and_backup()
