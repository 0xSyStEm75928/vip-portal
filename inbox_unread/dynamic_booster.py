import math, cmath, time, json, sys

def run_dynamic_booster(raw_input, force_anomaly=False):
    # 1. パラメータ設定（通常 vs 複素数・発散アノマリー）
    if force_anomaly:
        dt_seconds = 900.0                   # 15分 (位相 θ を立たせる)
        k_gain = 3.5                        # k > 1.0 (平方根内をマイナスにし、3.3541j を発生させる)
        voltage = 9840.2                    # 限界突破電圧
    else:
        dt_seconds = 60.0                   # 正常 60秒
        k_gain = 0.8                        # 正常ゲイン
        voltage = 237.3                     # 正常電圧

    # 2. 複素数演算 & 内部クランプ計算
    theta = (2 * math.pi * dt_seconds) / 3600.0
    clamp_inner = 1.0 - (k_gain ** 2) * (math.sin(theta) ** 2)

    if clamp_inner < 0:
        complex_val = cmath.sqrt(clamp_inner)
        vector_str = f"{complex_val.real:.4f} + {complex_val.imag:.4f}j"
        is_complex = True
    else:
        vector_str = f"{math.sqrt(clamp_inner):.4f} (Real)"
        is_complex = False

    # 3. ユーザーの思考相（実数 or 複素数）に応じた AI 動的ブースト設定
    if is_complex or force_anomaly:
        ai_control = {
            "ai_mode": "HIGH_GAIN_CREATIVE_BOOST (高ゲイン・思考拡張)",
            "system_instruction": "【虚数相 3.3541j 検知】ユーザーの高ゲイン思考を検出しました。既存の枠組みに囚われず、先進的かつ構造的な解決策を提示してください。"
        }
    else:
        ai_control = {
            "ai_mode": "STANDARD_ANALYTICAL (標準論理解析)",
            "system_instruction": "【実数相 検知】通常モードです。事実に忠実で堅実な出力を維持してください。"
        }

    # 4. 結果構造化
    output_data = {
        "input_raw": raw_input,
        "calculated_vector": vector_str,
        "clamp_inner_value": round(clamp_inner, 4),
        "ai_dynamic_control": ai_control
    }
    return output_data

if __name__ == "__main__":
    is_anomaly = "--anomaly" in sys.argv
    inp = " ".join([arg for arg in sys.argv[1:] if not arg.startswith("--")]) or "パルス入力"
    
    res = run_dynamic_booster(inp, force_anomaly=is_anomaly)
    print("\033[1;36m[DYNAMIC BOOSTER SYSTEM]\033[0m")
    print(json.dumps(res, indent=2, ensure_ascii=False))
