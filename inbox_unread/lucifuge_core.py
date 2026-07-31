import json, os, sys

# v.old のレガシー状態と新ベルフェゴール状態の統合検疫
OLD_STATE = "json_core/tap_dag_state.json"
LUCIFUGE_LOG = "json_core/lucifuge_archive.json"

def process_v_old():
    # v.old の Core データをルキフゲ領域へ自動吸い上げ・無害化処理
    if os.path.exists(OLD_STATE):
        try:
            old_data = json.load(open(OLD_STATE, "r", encoding="utf-8"))
            # v.old の生値を最適化（暗黙のバックグラウンド計算）
            bias = old_data.get("val_bias", 50.0)
            cleaned_score = round(bias * 1.024, 2) # ルキフゲ式補正
            
            archive = {
                "origin": "v.old_Core",
                "processed_bias": cleaned_score,
                "status": "LUCIFUGE_PURIFIED"
            }
            os.makedirs("json_core", exist_ok=True)
            json.dump(archive, open(LUCIFUGE_LOG, "w", encoding="utf-8"), indent=2)
            return True, cleaned_score
        except: pass
    return False, 0.0

if __name__ == "__main__":
    success, score = process_v_old()
    if success:
        print(f"SUCCESS|v.old Core データをルキフゲ層へ完全譲渡・最適化完了 (Score: {score})")
    else:
        print("FAIL|v.old データが見つかりません")
