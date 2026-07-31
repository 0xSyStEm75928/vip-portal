import time
import math
import random
import numpy as np
from pylsl import StreamInfo, StreamOutlet

def main():
    # 4チャンネル / 250Hz のLSLストリームを定義
    info = StreamInfo('EEG_Simulation_V2', 'EEG', 4, 250, 'float32', 'sim_v2_id')
    outlet = StreamOutlet(info)

    print("--- 安定版 EEG/Power 統合シミュレーター起動 (Ctrl+C で停止) ---")
    
    t = 0.0
    fs = 250.0  # サンプリング周波数 [Hz]
    dt = 1.0 / fs
    r_ohms = 1000.0  # 仮想負荷抵抗 1kΩ

    try:
        while True:
            # --- 1. 信号合成 (アルファ波:8-12Hz + ベータ波:13-30Hz) ---
            alpha = 10.0 * math.sin(2 * math.pi * 10 * t)
            # ベータ波(V/B)の極端な跳ね上がりを防ぐため振幅上限を制御
            beta = 5.0 * math.sin(2 * math.pi * 20 * t)
            noise = random.gauss(0, 1.5)

            # 電圧値 (μV)
            v_ch1 = alpha + beta + noise
            v_ch2 = alpha * 0.8 + beta * 1.2 + noise
            v_ch3 = beta * 1.5 + noise
            v_ch4 = alpha * 1.1 + noise

            # 異常値のガード（-100μV 〜 +100μV に制限）
            sample = [np.clip(v, -100.0, 100.0) for v in [v_ch1, v_ch2, v_ch3, v_ch4]]

            # --- 2. LSLストリームへ送信 ---
            outlet.push_sample(sample)

            # --- 3. 瞬間電力・RMSの算出 (Ch1をベースに計算) ---
            rms_uv = abs(sample[0])
            power_nw = (((rms_uv * 1e-6) ** 2) / r_ohms) * 1e9  # [nW]

            # ターミナルへリアルタイム表示 (100msごとに描画更新)
            if int(t * fs) % 25 == 0:
                print(f"[{t:6.2f}s] Ch1: {sample[0]:6.2f} uV | Beta/Noise Ctrl: OK | Power: {power_nw:8.5f} nW", end="\r")

            time.sleep(dt)
            t += dt

    except KeyboardInterrupt:
        print("\nシミュレーションを停止し、破棄しました。")

if __name__ == "__main__":
    main()
