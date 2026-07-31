import time
import math

class TypingBiometricDetector:
    def __init__(self, r_ohm=1000.0):
        self.r_ohm = r_ohm
        self.last_timestamp = None
        self.intervals = []
        self.max_history = 10

    def register_keystroke(self, input_text):
        now = time.time()
        
        # 初回打鍵の初期化処理
        if self.last_timestamp is None:
            self.last_timestamp = now
            return None

        # 1. 物理メトリクス算出: 打鍵間隔（dt）
        dt = now - self.last_timestamp
        self.last_timestamp = now
        
        # 履歴バッファの更新
        self.intervals.append(dt)
        if len(self.intervals) > self.max_history:
            self.intervals.pop(0)

        # 2. 統計量算出（平均・ジッター/揺らぎ・推定WPM）
        mean_dt = sum(self.intervals) / len(self.intervals)
        
        # ジッター（打鍵間隔の分散/揺らぎ）：メンタルの揺らぎ指標
        variance = sum((x - mean_dt) ** 2 for x in self.intervals) / len(self.intervals)
        jitter = math.sqrt(variance)
        
        # タイピング速度（WPM相当）
        wpm = (60.0 / mean_dt) if mean_dt > 0 else 0.0

        # 3. 入力間隔を擬似脳波電圧（uV）および電力（nW）へ変換
        # 高速・安定入力 = 低電圧・安定 / 入力停滞・乱れ = 電圧スパイク
        voltage_uv = (jitter * 50.0) + (10.0 / (mean_dt + 0.1))
        voltage_v = voltage_uv * 1e-6
        power_nw = ((voltage_v ** 2) / self.r_ohm) * 1e9

        return {
            "dt": dt,
            "mean_dt": mean_dt,
            "jitter": jitter,
            "wpm": wpm,
            "voltage_uv": voltage_uv,
            "power_nw": power_nw,
            "char_len": len(input_text)
        }

def main():
    detector = TypingBiometricDetector()
    print("=== 打鍵タイミング・過渡状態 検出エンジン起動 ===")
    print(">> 何か文字（コマンドやEnter）を入力するたびに、打鍵間隔や揺らぎを検出します。")
    print(">> 終了するには 'exit' と入力するか Ctrl+C を押してください。\n")

    try:
        while True:
            user_input = input("\033[1;34m[INPUT]>\033[0m ")
            if user_input.strip().lower() == "exit":
                print("\n[INFO] 検出セッションを終了しました。")
                break

            metrics = detector.register_keystroke(user_input)
            
            if metrics is None:
                print(" >> [INIT] 初回入力検知。次回入力からインターバル測定を開始します。\n")
                continue

            # 状態判定（メンタル・タイピングポジション）
            if metrics["jitter"] < 0.15 and metrics["wpm"] > 80:
                state_str = "\033[1;32m[HIGH-FLOW / STABLE]\033[0m"
            elif metrics["jitter"] > 0.5:
                state_str = "\033[1;31m[HESITATION / HIGH-JITTER]\033[0m"
            else:
                state_str = "\033[1;36m[NOMINAL FOCUS]\033[0m"

            # 検出結果のリアルタイム表示
            print(f" ├─► Interval (dt) : {metrics['dt']:6.3f} sec | Avg: {metrics['mean_dt']:6.3f} sec")
            print(f" ├─► Jitter (揺らぎ) : {metrics['jitter']:6.3f} | Speed: {metrics['wpm']:5.1f} WPM")
            print(f" └─► Equiv. Voltage: {metrics['voltage_uv']:6.2f} uV | Power: {metrics['power_nw']:9.6f} nW | State: {state_str}\n")

    except KeyboardInterrupt:
        print("\n[INFO] 割り込み検知。セッションを安全に閉鎖しました。")

if __name__ == "__main__":
    main()
