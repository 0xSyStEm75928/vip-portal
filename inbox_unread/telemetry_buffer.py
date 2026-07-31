import time
import math
import json

class ManualAnalysisEngine:
    def __init__(self):
        self.config = {
            "spike_gwei_threshold": 100.0,
            "jitter_sensitivity": 1.5,
            "staging_timeout_sec": 2.5,
            "silent_mode": True
        }
        self.history_log = []

    def set_param(self, key, value):
        if key in self.config:
            target_type = type(self.config[key])
            if target_type == bool:
                self.config[key] = value.lower() in ("true", "1", "yes")
            else:
                self.config[key] = target_type(value)
            print(f"[PARAM UPDATED] {key} --> {self.config[key]}")
        else:
            print(f"[ERROR] 未定義のパラメータです: {key}")

    def analyze_manual_event(self, dt, jitter, gwei, spread_pct):
        smoothed_jitter = math.log1p(min(jitter, 50.0))
        voltage_uv = min(120.0, (smoothed_jitter * 35.0) + (10.0 / (dt + 0.05)))
        
        is_gwei_spike = gwei >= self.config["spike_gwei_threshold"]
        ghost_target = None
        if is_gwei_spike:
            pressure = gwei / self.config["spike_gwei_threshold"]
            ghost_target = spread_pct * (1.0 + math.log1p(pressure) * 4.0)

        is_revert = jitter > self.config["jitter_sensitivity"]
        
        result = {
            "dt": dt,
            "jitter": jitter,
            "voltage_uv": voltage_uv,
            "gwei": gwei,
            "is_spike": is_gwei_spike,
            "ghost_target": ghost_target,
            "is_revert": is_revert,
            "silent_view": self.config["silent_mode"]
        }
        self.history_log.append(result)
        return result

def main():
    engine = ManualAnalysisEngine()
    print("=== MANUAL OVERRIDE & ANALYZER ENGINE ===")
    print(">> 手動コマンド例:")
    print("   set spike_gwei_threshold 120.0  -> スパイク閾値を120 Gweiに変更")
    print("   set jitter_sensitivity 2.0      -> Jitter感度を変更")
    print("   eval 0.15 1.8 140 12            -> [dt] [jitter] [gwei] [spread%] を手動分析")
    print("   dump                            -> これまでの手動分析ログを表示")
    print("   exit                            -> 終了\n")

    while True:
        try:
            raw = input("[MANUAL-CONSOLE]> ").strip().split()
            if not raw:
                continue
            cmd = raw[0].lower()

            if cmd == "exit":
                print("[INFO] 手動アナライザーを終了します。")
                break
            elif cmd == "set" and len(raw) == 3:
                engine.set_param(raw[1], raw[2])

            elif cmd == "eval" and len(raw) == 5:
                dt = float(raw[1])
                jit = float(raw[2])
                gwei = float(raw[3])
                spr = float(raw[4])
                
                res = engine.analyze_manual_event(dt, jit, gwei, spr)
                print(f" |- 電圧応答: {res['voltage_uv']:.2f} uV | Gweiスパイク: {res['is_spike']}")
                if res['ghost_target']:
                    print(f" |- [TARGET GHOST SPREAD] 潜在スプレッド: {res['ghost_target']:.2f}%")
                
                status = "[REVERT (拒絶)]" if res['is_revert'] else "[CONFIRM (承認)]"
                print(f" +- 判定ステータス: {status} (SilentView: {res['silent_view']})\n")

            elif cmd == "dump":
                print(json.dumps(engine.history_log, indent=2))

            else:
                print("[!] コマンド構文エラーです。例: eval 0.15 1.8 140 12")

        except Exception as e:
            print(f"[ERROR] 解析処理に失敗しました: {e}")

if __name__ == "__main__":
    main()
