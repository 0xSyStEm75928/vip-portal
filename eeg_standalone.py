import time
import math
import random

class StandaloneEEGSimulator:
    def __init__(self, fs=250.0, n_channels=4):
        self.fs = fs
        self.n_channels = n_channels
        self.impedance_ohm = 1000.0  # 皮下・頭皮抵抗 R = 1.0 kΩ
        
        # 1次IIRハイパスフィルタ (DCドリフトカット: fc ~0.5Hz)
        dt = 1.0 / self.fs
        rc = 1.0 / (2 * math.pi * 0.5)
        self.alpha_hp = rc / (rc + dt)
        self.prev_raw = [0.0] * self.n_channels
        self.prev_hp = [0.0] * self.n_channels

    def generate_signal(self, t):
        """ 生理学的シグナル合成 (Alpha: 10Hz, Beta: 20Hz + DC Offset) """
        alpha = 15.0 * math.sin(2 * math.pi * 10.0 * t)
        beta_mod = 1.0 + 0.3 * math.sin(2 * math.pi * 0.1 * t)
        beta = 8.0 * beta_mod * math.sin(2 * math.pi * 20.0 * t)
        dc_offset = 25.0
        
        channels = [
            alpha + beta + dc_offset + random.gauss(0, 2.0),
            alpha * 0.7 + beta * 1.4 + dc_offset + random.gauss(0, 2.0),
            beta * 1.8 + dc_offset + random.gauss(0, 2.0),
            alpha * 1.2 + dc_offset + random.gauss(0, 2.0)
        ]
        return channels

    def filter_signal(self, raw_channels):
        """ 1次IIRハイパスフィルタ処理 """
        filtered = []
        for i in range(self.n_channels):
            hp = self.alpha_hp * (self.prev_hp[i] + raw_channels[i] - self.prev_raw[i])
            self.prev_raw[i] = raw_channels[i]
            self.prev_hp[i] = hp
            filtered.append(hp)
        return filtered

    def calculate_power(self, voltage_uv):
        """ 物理量の変換: μV -> V -> nW (P = V^2 / R) """
        voltage_v = voltage_uv * 1e-6
        power_watts = (voltage_v ** 2) / self.impedance_ohm
        return power_watts * 1e9  # [nW]

def main():
    sim = StandaloneEEGSimulator(fs=250.0, n_channels=4)
    print("=== 完全ゼロ依存（標準ライブラリのみ）EEG 処理シミュレーター起動 ===")
    print(f"Sampling: {sim.fs} Hz | Channels: {sim.n_channels} | Impedance: {sim.impedance_ohm} Ω")
    print("----------------------------------------------------------------------")
    
    dt = 1.0 / sim.fs
    t = 0.0
    
    try:
        while True:
            raw_data = sim.generate_signal(t)
            filtered_data = sim.filter_signal(raw_data)
            power_nw = sim.calculate_power(filtered_data[0])
            
            # ターミナルへリアルタイム描画 (10Hz更新)
            if int(round(t * sim.fs)) % 25 == 0:
                ch1_v = filtered_data[0]
                ch2_v = filtered_data[1]
                print(f"[{t:6.2f}s] Ch1: {ch1_v:6.2f} uV | Ch2: {ch2_v:6.2f} uV | Inst. Power: {power_nw:9.6f} nW", end="\r")
                
            time.sleep(dt)
            t += dt
            
    except KeyboardInterrupt:
        print("\n[INFO] 実験セッションを安全に終了しました。")

if __name__ == "__main__":
    main()
