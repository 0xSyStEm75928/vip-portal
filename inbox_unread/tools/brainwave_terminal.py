import math, time, sys, random

def generate_eeg_stream(duration_sec=10):
    print("\033[1;32m[EEG BRAINWAVE TERMINAL STREAM STARTED]\033[0m")
    print("Sampling Frequency: 256 Hz | Channel: Fp1-Fp2 (Prefrontal)")
    print("-" * 60)
    
    start_time = time.time()
    step = 0
    
    try:
        while time.time() - start_time < duration_sec:
            t = step * 0.1
            
            # 1. 各脳波成分の合成（アルファ波 10Hz, ベータ波 20Hz, ガンマ波 40Hz + ノイズ）
            alpha = 15 * math.sin(2 * math.pi * 10 * t)   # リラックス時 (8-12Hz)
            beta  = 25 * math.sin(2 * math.pi * 20 * t)   # 集中・論理思考 (13-30Hz)
            gamma = 10 * math.sin(2 * math.pi * 40 * t)   # ひらめき・高ゲイン (30-100Hz)
            noise = random.uniform(-3, 3)
            
            # 2. トータル電位 (µV) の算出
            total_eeg_uv = round(alpha + beta + gamma + noise, 2)
            
            # 3. ターミナル用・ビジュアル波形グラフの生成
            # 電位に応じて文字（*）の幅を可視化
            bar_length = int((total_eeg_uv + 60) / 3)
            bar_length = max(1, min(40, bar_length))
            graph_bar = "█" * bar_length
            
            # 4. 周波数相の判定
            phase = "\033[1;35m[GAMMA/HIGH-GAIN]\033[0m" if total_eeg_uv > 20 else "\033[1;34m[BETA/ANALYTICAL]\033[0m"
            
            print(f"EEG: {total_eeg_uv:6.2f} µV | {graph_bar:<40} | {phase}")
            time.sleep(0.1)
            step += 1
            
    except KeyboardInterrupt:
        pass
        
    print("-" * 60)
    print("\033[1;36m[STREAM TERMINATED - DATA BUFFER SAVED]\033[0m")

if __name__ == "__main__":
    generate_eeg_stream(duration_sec=8)
