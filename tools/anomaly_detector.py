import math, time, json, sys, cmath

def run_anomaly_simulation(raw_input, force_anomaly=False):
    current_time = time.time()
    
    # 1. パラメータのセット（異常モード時は臨界閾値を突破させる）
    if force_anomaly:
        dt_seconds = 0.000001               # Delta t -> 0 (ゼロ除算・無限大発散を引き起こす)
        k_gain = 3.5                        # k > 1.0 (平方根内を負数にし、複素数 i を発生させる)
        voltage = 9840.2                    # 3.3V(3300mV) 限界突破
    else:
        dt_seconds = 60.0                   # 正常な時間経過 (60秒)
        k_gain = 0.8                        # 正常範囲のゲイン (k < 1.0)
        voltage = 237.3                     # 正常電圧 (237.3mV)

    # 2. 数値計算（実数 ＆ 複素数演算）
    text_len = len(raw_input)
    phi_p = math.log(1 + text_len) * 10 if force_anomaly else math.log(1 + text_len)
    
    # 時間波形クランプ演算: sqrt(1 - k^2 * sin^2(theta))
    theta = (2 * math.pi * dt_seconds) / 3600.0
    sin_val = math.sin(theta)
    clamp_inner = 1.0 - (k_gain ** 2) * (sin_val ** 2)

    # 平方根内の判定（負数の場合は cmath による複素数計算へ遷移）
    if clamp_inner < 0:
        complex_clamp = cmath.sqrt(clamp_inner)
        complex_str = f"{complex_clamp.real:.4f} + {complex_clamp.imag:.4f}i"
        phase_status = "COMPLEX_PHASE_SHIFT (虚数空間へ遷移)"
    else:
        complex_str = f"{math.sqrt(clamp_inner):.4f} (Real)"
        phase_status = "REAL_DOMAIN (実数領域)"

    # 無限大発散 (INF) の判定
    try:
        score_val = phi_p / dt_seconds
        score_str = f"{score_val:.4f}"
    except ZeroDivisionError:
        score_str = "INF (Infinity / 無限大発散)"

    if dt_seconds < 0.001:
        score_str = "INF (Unbounded Divergence / 発散)"

    # 3. 観測ログJSONの構造化
    telemetry = {
        "execution_mode": "ANOMALY_BREAKTHROUGH" if force_anomaly else "NORMAL_STABLE",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(current_time)),
        "parameters": {
            "delta_t": dt_seconds,
            "k_gain": k_gain,
            "measured_voltage_mv": voltage
        },
        "observed_metrics": {
            "phase_status": phase_status,
            "future_prediction_score": score_str,
            "wave_clamp_vector": complex_str,
            "safety_clamp": "BROKEN (Exceeded 3300mV)" if voltage > 3300 else "NORMAL_CLAMPED"
        }
    }
    return telemetry

if __name__ == "__main__":
    mode_flag = "--anomaly" in sys.argv
    inp = " ".join([arg for arg in sys.argv[1:] if not arg.startswith("--")]) or "臨界試験用インパルス"
    
    result = run_anomaly_simulation(inp, force_anomaly=mode_flag)
    
    print("\033[1;33m[ANOMALY DETECTOR OUTPUT]\033[0m")
    print(json.dumps(result, indent=2, ensure_ascii=False))
