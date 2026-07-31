import json, time, os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_STORE = os.path.join(BASE_DIR, "data_store")

class JSONCodeSmith:
    @staticmethod
    def forge_armored_json(raw_data, device_id="MOBILE_DEV_01"):
        """ 生の内蔵JSONを受け取り、頑丈な「外装化（Armored）」を施す """
        
        # 1. 内蔵コアデータのサニタイズ＆構造チェック
        raw_str = json.dumps(raw_data, ensure_ascii=False)
        if "<script>" in raw_str or "exec(" in raw_str:
            print("\033[1;31m[404 SILENT KILL]\033[0m 危険なコアデータを検知。外装化を拒否して破棄します。")
            return None

        # 2. 外装（Outer Armor）の装着
        armored_payload = {
            "$schema": "armored.mobile.json/v1",
            "_armor_meta": {
                "forged_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "target_device": device_id,
                "integrity_hash": hash(raw_str),
                "armor_status": "LOCKED_AND_PROTECTED"
            },
            "_inner_core": raw_data  # 保護された内蔵コアデータ
        }
        
        return armored_payload

def build_mobile_package():
    sample_inner_data = {
        "user_id": "VIP_Client_Alpha",
        "action": "FETCH_SECRET_STREAM",
        "status": "ACTIVE"
    }

    print("\033[1;36m[SMITH FORGING]\033[0m 内蔵JSONデータの外装化（プロテクト）を開始します...")
    armored = JSONCodeSmith.forge_armored_json(sample_inner_data)

    if armored:
        output_path = os.path.join(DATA_STORE, "armored_mobile_output.json")
        os.makedirs(DATA_STORE, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(armored, f, ensure_ascii=False, indent=2)
        
        print("\033[1;32m[ARMORED SUCCESS]\033[0m 外装プロテクト済みJSONの鋳造（Forge）完了！")
        print(f"📁 保存先: {output_path}")

if __name__ == "__main__":
    build_mobile_package()
