import time
import math
import sys

class NeuralMEVEngine:
    def __init__(self):
        self.r_ohm = 1000.0
        self.last_ts = None
        self.intervals = []
        self.max_hist = 6
        
        # 脳波伝導スマホ プロファイルステータス (Cyberpunk Data Model)
        self.profile = {
            "bio_sig": "NEURAL-SYNC-909",
            "sync_rate": 100.0,        # 同調率 (%)
            "neural_load": 0.0,        # 脳波負荷 (nW)
            "overdrive_unlocked": True
        }

    def simulate_tx(self, raw_command, now):
        """ MEVスタイル: トランザクション実行前の生体シミュレーション """
        if self.last_ts is None:
            self.last_ts = now
            return {"status": "MEMPOOL_INIT", "revert": False}

        dt = now - self.last_ts
        self.last_ts = now
        
        self.intervals.append(dt)
        if len(self.intervals) > self.max_hist:
            self.intervals.pop(0)

        n = len(self.intervals)
        mean_dt = sum(self.intervals) / float(n)
        variance = sum((x - mean_dt) ** 2 for x in self.intervals) / float(n)
        jitter = math.sqrt(max(0.0, variance))

        # 生体過渡応答計算
        smoothed_jitter = math.log(1.0 + min(jitter, 50.0))
        voltage_uv = min(120.0, (smoothed_jitter * 35.0) + (10.0 / (mean_dt + 0.05)))
        power_nw = (((voltage_uv * 1e-6) ** 2) / self.r_ohm) * 1e9

        # サイバーパンク・プロファイルの更新
        self.profile["sync_rate"] = max(10.0, 100.0 - (jitter * 15.0))
        self.profile["neural_load"] = power_nw

        # --- MEV REVERT 判定条件 ---
        # 1. 極度の焦り/迷い (Jitter > 2.5) -> トランザクション・リバート
        # 2. 長考直後の不規則爆発 -> シミュレーション失敗としてロールバック
        is_revert = (jitter > 2.5) or (voltage_uv > 90.0)

        return {
            "dt": dt,
            "jitter": jitter,
            "voltage_uv": voltage_uv,
            "power_nw": power_nw,
            "revert": is_revert,
            "reason": "HIGH_JITTER_MENTAL_INSTABILITY" if is_revert else "OK"
        }

def main():
    mev = NeuralMEVEngine()
    print("\033[1;36m=== NEURAL-MEV MEMPOOL & REVERT ENGINE (CYBERPUNK PROFILE) ===\033[0m")
    print("\033[1;33m>> Bio-Signature:\033[0m", mev.profile["bio_sig"])
    print(">> 打鍵の過渡状態を事前シミュレーションし、乱れを検知した場合はTXをRevert（無効化）します。\n")

    tx_nonce = 0

    try:
        while True:
            cmd = input(f"\033[1;35m[TX-MEMPOOL #{tx_nonce}]>\033[0m ").strip()
            if cmd.lower() == "exit":
                print("\n[INFO] MEV Engine Shutdown.")
                break

            now = time.time()
            res = mev.simulate_tx(cmd, now)

            if res["status"] == "MEMPOOL_INIT":
                print(" \033[1;30m├─► [MEMPOOL] 最初のトランザクションを受領。生体同期開始...\033[0m\n")
                tx_nonce += 1
                continue

            # MEV Revert 判定結果のログ出力
            print(f" ├─► [SIMULATION] dt: {res['dt']:5.3f}s | Jitter: {res['jitter']:5.3f} | SyncRate: {mev.profile['sync_rate']:5.1f}%")
            print(f" ├─► [BIO-METRICS] Voltage: {res['voltage_uv']:6.2f}uV | Power: {res['power_nw']:9.6f}nW")

            if res["revert"]:
                # トランザクション・リバート（実行キャンセル）
                print(f" \033[1;31m└─► [TX REVERTED] Reason: {res['reason']} (命令 '{cmd}' は破棄されました)\033[0m\n")
            else:
                # トランザクション承認（ブロック取り込み）
                print(f" \033[1;32m└─► [TX CONFIRMED] Block Executed: '{cmd}' (正常承認)\033[0m\n")

            tx_nonce += 1

    except (KeyboardInterrupt, EOFError):
        print("\n[INFO] Emergency Halt.")

if __name__ == "__main__":
    main()
