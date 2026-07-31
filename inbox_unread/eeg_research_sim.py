import time
import math
import random
from pylsl import StreamInfo, StreamOutlet

class EEGResearchSimulator:
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

        # LSL Stream Setup
        self.info = StreamInfo('EEG_Research_Stream', 'EEG', self.n_channels, self.fs, 'float32', 'eeg_res_001')
        self.outlet = StreamOutlet(self.info)

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
    sim = EEGResearchSimulator(fs=250.0, n_channels=4)
    print("=== ピュアPython版 EEG シミュレーター起動 ===")
    print(f"Sampling: {sim.fs} Hz | Channels: {sim.n_channels} | Impedance: {sim.impedance_ohm} Ω")
    
    dt = 1.0 / sim.fs
    t = 0.0
    
    try:
        while True:
            raw_data = sim.generate_signal(t)
            filtered_data = sim.filter_signal(raw_data)
            power_nw = sim.calculate_power(filtered_data[0])
            
            sim.outlet.push_sample(filtered_data)
            
            if int(t * sim.fs) % 25 == 0:
                print(f"[{t:6.2f}s] Ch1(Filtered): {filtered_data[0]:7.2f} uV | Inst. Power: {power_nw:10.7f} nW", end="\r")
                
            time.sleep(dt)
            t += dt
            
    except KeyboardInterrupt:
        print("\n[INFO] 実験セッションを終了。LSLストリームを切断しました。")

if __name__ == "__main__":
    main()
