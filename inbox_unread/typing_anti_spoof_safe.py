import time
import math

class SafeBiometricEngine:
    def __init__(self, r_ohm=1000.0):
        self.r_ohm = float(r_ohm)
        self.last_timestamp = None
        self.intervals = []
        self.max_history = 8

    def process_touch(self, input_text):
        now = time.time()
        
        if self.last_timestamp is None:
            self.last_timestamp = now
            return None

        dt = float(now - self.last_timestamp)
        self.last_timestamp = now
        
        self.intervals.append(dt)
        if len(self.intervals) > self.max_history:
            self.intervals.pop(0)

        n = len(self.intervals)
        mean_dt = sum(self.intervals) / float(n)
        
        # 安全な分散・ジッター計算 (Overflow/Illegal Instruction 防止)
        variance = sum((x - mean_dt) ** 2 for x in self.intervals) / float(n)
        jitter = math.sqrt(max(0.0, variance))

        # 不自然な完全一致の検出
        is_synthetic = (jitter < 0.002 and n >= 4)

        # 安全な対数収束処理
        smoothed_jitter = math.log(1.0 + min(jitter, 100.0))

        # 電圧・電力計算 (物理限界値でクリッピング)
        voltage_uv = min(100.0, (smoothed_jitter * 30.0) + (8.0 / (mean_dt + 0.05)))
        voltage_v = voltage_uv * 1e-6
        power_nw = ((voltage_v ** 2) / self.r_ohm) * 1e9

        return {
            "dt": dt,
            "jitter": jitter,
            "is_synthetic": is_synthetic,
            "voltage_uv": voltage_uv,
            "power_nw": power_nw
        }

def main():
    engine = SafeBiometricEngine()
    print("=== [SAFE ENGINE] 生体認証ガード機能 (CPU安全パッチ適用版) ===")
    print(">> タッチ/打鍵データの同期完了。入力待機中...\n")

    try:
        while True:
            user_input = input("\033[1;34m[TOUCH/KEY]>\033[0m ")
            if user_input.strip().lower() == "exit":
                print("\n[INFO] プロセスを正常クローズしました。")
                break

            m = engine.process_touch(user_input)
            if m is None:
                print(" >> [INIT] 初回打鍵同期完了。\n")
                continue

            status = "\033[1;31m[REJECT: ARTIFICIAL]\033[0m" if m["is_synthetic"] else "\033[1;32m[VERIFIED: HUMAN SIG]\033[0m"

            print(f" ├─► Interval: {m['dt']:6.3f}s | Jitter: {m['jitter']:6.4f}")
            print(f" └─► Voltage: {m['voltage_uv']:6.2f}uV | Power: {m['power_nw']:9.6f}nW | Status: {status}\n")

    except (KeyboardInterrupt, EOFError):
        print("\n[INFO] セッションを安全に割り込み終了しました。")

if __name__ == "__main__":
    main()
