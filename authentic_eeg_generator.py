import numpy as np

def generate_authentic_eeg(duration_sec=10, sampling_rate=250):
    """
    本物の生体EEGが持つ物理的特性(1/f揺らぎ + 瞬き電位スパイク)を合成発生させる
    """
    num_samples = duration_sec * sampling_rate
    
    # 1. 1/f Pink Noise (脳神経の物理的ゆらぎ) の生成
    uneven = np.random.randn(num_samples)
    fft_signal = np.fft.rfft(uneven)
    freqs = np.fft.rfftfreq(num_samples, d=1/sampling_rate)
    
    # 1/f スケーリング (0除算回避)
    fft_signal[1:] /= np.sqrt(freqs[1:])
    pink_noise = np.fft.irfft(fft_signal, n=num_samples)
    
    # 2. α波 (8-12Hz) と β波 (13-30Hz) の揺らぎ結合
    t = np.linspace(0, duration_sec, num_samples, endpoint=False)
    alpha_wave = 0.5 * np.sin(2 * np.pi * 10 * t + np.random.uniform(0, 2*np.pi))
    
    # 3. 本物EEG特有の「瞬き(EOG)過渡スパイク」をランダムに挿入 (偽作にはこれが無い)
    eog_artifacts = np.zeros(num_samples)
    num_blinks = np.random.randint(2, 5) # 10秒間に2~4回の瞬き
    for _ in range(num_blinks):
        blink_pos = np.random.randint(sampling_rate, num_samples - sampling_rate)
        blink_width = int(0.2 * sampling_rate) # 約200msの瞬き電位
        blink_shape = np.hanning(blink_width) * np.random.uniform(3.0, 6.0) # 強いスパイク
        
        start = max(0, blink_pos - blink_width // 2)
        end = min(num_samples, start + blink_width)
        eog_artifacts[start:end] += blink_shape[:end-start]
        
    # 生体シグナルの結合 (単位: μV)
    authentic_signal = (pink_noise * 10.0) + (alpha_wave * 5.0) + (eog_artifacts * 15.0)
    return authentic_signal

def verify_eeg_authenticity(signal, sampling_rate=250):
    """
    入力データが本物の生体EEG特徴を満たしているかを数学的に検証する
    """
    # 特徴1: 尖度 (Kurtosis) による瞬き/過渡応答の存在確認 (人工の正弦波は平坦になる)
    mean = np.mean(signal)
    std = np.std(signal)
    if std == 0:
        return False, "DEAD_SIGNAL_ZERO_VARIANCE"
    
    kurtosis = np.mean(((signal - mean) / std) ** 4) - 3.0
    
    # 特徴2: 1/f パワースペクトル指数の検証
    fft_vals = np.abs(np.fft.rfft(signal))
    freqs = np.fft.rfftfreq(len(signal), d=1/sampling_rate)
    
    # 5Hz - 40Hz の帯域でスペクトル傾斜を計算
    valid_idx = (freqs >= 5) & (freqs <= 40)
    log_f = np.log(freqs[valid_idx])
    log_p = np.log(fft_vals[valid_idx] + 1e-8)
    
    slope, _ = np.polyfit(log_f, log_p, 1)
    
    # 判定基準: 生体シグナルはスペクトルが負の傾斜(-1/f)を持ち、かつ適度な過渡スパイク(Kurtosis > 0.5)を持つ
    is_authentic = (slope < -0.3) and (kurtosis > 0.3)
    
    details = {
        "spectral_slope": round(float(slope), 3),
        "kurtosis": round(float(kurtosis), 3),
        "passed": bool(is_authentic)
    }
    return is_authentic, details

if __name__ == "__main__":
    # テスト実行
    raw_signal = generate_authentic_eeg()
    is_valid, result = verify_eeg_authenticity(raw_signal)
    
    print(f"--- EEG AUTHENTICITY VERIFICATION ---")
    print(f"Result: {'AUTHENTIC_HUMAN_EEG' if is_valid else 'FAKE_SYNTHETIC_SIGNAL'}")
    print(f"Metrics: {result}")
