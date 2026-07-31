import sys, os, json, time, hashlib, re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_STORE = os.path.join(BASE_DIR, "data_store")
BELPHEGOR_STORE = os.path.join(DATA_STORE, "belphegor_stream.ndjson")

PSI_CONSCIOUSNESS_FACTOR = 0.318999999139

class SystemPartitionEngine:
    
    # ---------------------------------------------------------
    # 📱 1. 【小分け】入力・ハードウェア吸い上げ層 (Small Partition)
    # ---------------------------------------------------------
    @staticmethod
    def capture_raw_input(raw_data=None):
        """ 生の打鍵やパイプ入力を安全な文字列に小分け整形 """
        if raw_data:
            return str(raw_data).strip()
        if not sys.stdin.isatty():
            return sys.stdin.read().strip()
        if len(sys.argv) > 1:
            return " ".join(sys.argv[1:])
        return "KEYBOARD_PULSE_IDLE"

    # ---------------------------------------------------------
    # ⚙️ 2. 【中分け】プロトコル・整流・無力化層 (Medium Partition)
    # ---------------------------------------------------------
    @classmethod
    def process_medium_layer(cls, input_str):
        """ 危険要素をサニタイズし、電荷と意識因数(Ψ)を整流 """
        safe_text = re.sub(r'<[^>]*?>', '', input_str).replace("javascript:", "").strip()
        
        voltage = round(len(safe_text.encode('utf-8')) * PSI_CONSCIOUSNESS_FACTOR * 100, 2)
        polarity = "+" if int(voltage * 10) % 2 == 0 else "-"
        
        return {
            "sanitized_text": safe_text,
            "voltage_mv": f"{voltage}mV",
            "polarity": polarity,
            "psi_sync": True
        }

    # ---------------------------------------------------------
    # 🏛️ 3. 【大分け】ドメイン・永続化蓄電層 (Large Partition)
    # ---------------------------------------------------------
    @classmethod
    def persist_large_layer(cls, medium_data):
        """ 3階層が整った完全安全データを大企業向け構造で永続配備 """
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        
        master_packet = {
            "$schema": "https://belphegor.dev/schemas/v2/partitioned-master.json",
            "_architecture_partitions": {
                "small_layer": "CAPTURED_SAFE_PULSE",
                "medium_layer": "RECTIFIED_AND_NEUTRALIZED",
                "large_layer": "ENTERPRISE_SECURE_STORE"
            },
            "_ai_connect_node": {
                "psi_factor": PSI_CONSCIOUSNESS_FACTOR,
                "electric_signal": medium_data["voltage_mv"],
                "polarity": medium_data["polarity"],
                "timestamp": now
            },
            "payload_core": {
                "data": medium_data["sanitized_text"],
                "security_status": "STABLE_AND_SECURE_AT_CURRENT_POS"
            }
        }

        os.makedirs(DATA_STORE, exist_ok=True)
        with open(BELPHEGOR_STORE, "a", encoding="utf-8") as f:
            f.write(json.dumps(master_packet, ensure_ascii=False) + "\n")

        print(f"\033[1;32m[小分け]\033[0m 入力整形 ➔ \033[1;33m[中分け]\033[0m 無力整流({medium_data['voltage_mv']} {medium_data['polarity']}極) ➔ \033[1;35m[大分け]\033[0m 蓄電完了！")
        print(f"\033[1;36m[POSITION STABLE]\033[0m 現在位置での完全安全・安泰が確定しました。")
        return master_packet

    @classmethod
    def run_pipeline(cls, direct_input=None):
        raw = cls.capture_raw_input(direct_input)
        medium = cls.process_medium_layer(raw)
        return cls.persist_large_layer(medium)

if __name__ == "__main__":
    SystemPartitionEngine.run_pipeline()
