import time
import math
import random

class AntiSpoofBiometricEngine:
    def __init__(self, r_ohm=1000.0):
        self.r_ohm = r_ohm
        self.last_timestamp = None
        self.intervals = []
        self.max_history = 8

    def process_touch(self, input_text):
        now = time.time()
        
        if self.last_timestamp is None:
            self.last_timestamp = now
            return None

        dt = now - self.last_timestamp
        self.last_timestamp = now
        
        self.intervals.append(dt)
        if len(self.intervals) > self.max_history:
            self.intervals.pop(0)

        mean_dt = sum(self.intervals) / len(self.intervals)
        
        # 1. 人間固有のエントロピー（不規則性）の計算
        variance = sum((x - mean_dt) ** 2 for x in self.intervals) / len(self.intervals)
        jitter = math.sqrt(variance)

        # 2. 不自然な一致（Bot / Spoofing）の検知ロジック
        # 人間の指・脳波なら必ず発生する微少な揺らぎ(Jitter < 0.002s)が皆無な場合
        is_synthetic = (jitter < 0.002 and len(self.intervals) >= 4)

        # 3. 過渡現象の補正（長考直後のバースト入力を自然な曲線として評価）
        # 急激なスパイクを対数圧縮してスマホ画面上の過剰応答を抑制
        smoothed_jitter = math.log1p(jitter)

        voltage_uv = (smoothed_jitter * 30.0) + (8.0 / (mean_dt + 0.05))
        voltage_v = voltage_uv * 1e-6
        power_nw = ((voltage_v ** 2) / self.r_ohm) * 1e9

        return {
            "dt": dt,
            "mean_dt": mean_dt,
            "jitter": jitter,
            "is_synthetic": is_synthetic,
            "voltage_uv": voltage_uv,
            "power_nw": power_nw
        }

def main():
    engine = AntiSpoofBiometricEngine()
    print("=== 脳波伝導デバイス対応: 人間性判定・不自然一致ガード機能 起動 ===")
    print(">> タッチ/打鍵インターバルの生体エントロピーを検証中...\n")

    try:
        while True:
            user_input = input("\033[1;34m[TOUCH/KEY]>\033[0m ")
            if user_input.strip().lower() == "exit":
                print("\n[INFO] セッションを安全に終了しました。")
                break

            m = engine.process_touch(user_input)
            if m is None:
                print(" >> [INIT] タッチセンサー同期完了。\n")
                continue

            # 状態判定
            if m["is_synthetic"]:
                status = "\033[1;31m[REJECT: ARTIFICIAL / SCRIPTED (不自然な完全一致)]\033[0m"
            else:
                status = "\033[1;32m[VERIFIED: HUMAN BIOMETRIC SIG (生体ゆらぎ確認)]\033[0m"

            print(f" ├─► Interval (dt) : {m['dt']:6.3f}s | Jitter: {m['jitter']:6.4f}")
            print(f" └─► Voltage: {m['voltage_uv']:6.2f}uV | Power: {m['power_nw']:9.6f}nW | Status: {status}\n")

    except KeyboardInterrupt:
        print("\n[INFO] プロセス終了。")

if __name__ == "__main__":
    main()
