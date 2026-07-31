import numpy as np

def calculate_signal_power(voltage_samples_uv):
    """
    電圧サンプル列(μV)から実効値(RMS)および相対電力(Power)を算出
    """
    arr = np.array(voltage_samples_uv)
    rms_voltage = np.sqrt(np.mean(arr**2))  # 実効電圧 [μV]
    
    # 仮想的な負荷抵抗 R = 1kΩ とした場合の瞬間最大電力(nWオーダー)の算出例
    r_ohms = 1000.0
    power_watts = ((rms_voltage * 1e-6) ** 2) / r_ohms
    
    return rms_voltage, power_watts

if __name__ == "__main__":
    # サンプルデータ (100個の電圧値)
    dummy_signal = np.random.normal(0, 15, 100) 
    
    rms, p_watts = calculate_signal_power(dummy_signal)
    print(f"信号RMS: {rms:.3f} uV")
    print(f"換算電力: {p_watts * 1e9:.6f} nW (ナノワット)")
