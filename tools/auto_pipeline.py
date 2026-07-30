import os, sys, json, time, subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INCOMING_DIR = os.path.join(BASE_DIR, "incoming_json")
DATA_STORE = os.path.join(BASE_DIR, "data_store")
MASTER_NDJSON = os.path.join(DATA_STORE, "optimized_master.ndjson")
V_OLD_DIR = os.path.join(DATA_STORE, "v.old")

def run_git_command(args):
    try:
        subprocess.run(["git"] + args, cwd=BASE_DIR, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def process_auto_pipeline(force_override=False):
    json_files = [f for f in os.listdir(INCOMING_DIR) if f.endswith('.json')]
    
    if not json_files:
        print("\033[1;33m[IDLE]\033[0m incoming_json に新規データはありません。")
        return

    os.makedirs(DATA_STORE, exist_ok=True)
    os.makedirs(V_OLD_DIR, exist_ok=True)

    # 次回のオーバーライド要求があるか、環境変数・引数で判定
    is_override = force_override or os.environ.get("OVERRIDE") == "1"

    if is_override:
        print("\033[1;35m[OVERRIDE MODE]\033[0m オートメーション手動による強制オーバーライドを発動。")
        if os.path.exists(MASTER_NDJSON):
            backup_name = f"override_backup_{int(time.time())}.ndjson"
            os.rename(MASTER_NDJSON, os.path.join(V_OLD_DIR, backup_name))
            print(f"\033[1;33m[BACKUP]\033[0m 旧マスターを {backup_name} に退避完了。")
    else:
        print("\033[1;36m[RIDE MODE]\033[0m 単なるライド（滑り込み）処理。マスターログを崩さずズレ込ませます。")

    processed_count = 0
    now_ts = int(time.time())

    for idx, file_name in enumerate(json_files):
        file_path = os.path.join(INCOMING_DIR, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            items = data if isinstance(data, list) else [data]
            
            mode = "w" if (is_override and processed_count == 0) else "a"
            with open(MASTER_NDJSON, mode, encoding="utf-8") as out_f:
                for offset, item in enumerate(items):
                    # ずれ込ませるためのミリ秒オフセットタイムスタンプ
                    staggered_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_ts + idx + offset))
                    record = {
                        "_processed_at": staggered_time,
                        "_mode": "OVERRIDE" if is_override else "RIDE",
                        "_origin_file": file_name,
                        "payload": item
                    }
                    out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    processed_count += 1

            os.remove(file_path)

        except Exception as e:
            print(f"\033[1;31m[404 SILENT KILL]\033[0m 不正データを排除: {file_name}")
            os.remove(file_path)

    print(f"\033[1;32m[SUCCESS]\033[0m {processed_count} 件を ({'OVERRIDE' if is_override else 'RIDE'}) で反映完了！")

    # Git同期
    run_git_command(["add", "."])
    commit_msg = f"auto(pipeline): {'override' if is_override else 'ride'} {processed_count} records"
    run_git_command(["commit", "-m", commit_msg])
    run_git_command(["push"])
    print("\033[1;32m[COMPLETE]\033[0m 全自動同期完了。")

if __name__ == "__main__":
    override_flag = sys.argv[1] == "--override" if len(sys.argv) > 1 else False
    process_auto_pipeline(override_flag)
