import sys, json, random, math

def audit_with_fluctuation(def_file_path):
    try:
        with open(def_file_path, 'r', encoding='utf-8') as f:
            user_def = json.load(f)
    except Exception as e:
        return {"error": f"定義ファイルの読み込み失敗: {str(e)}"}

    base_gain = float(user_def.get("gain", 1.0))
    base_depth = float(user_def.get("observation_depth", 5.0))
    mode = user_def.get("mode", "STANDARD")

    # 1. 揺れ幅（ゆらぎ）の生成
    # 観測深度(depth)が高いほど揺れ幅は小さくなり、現実(REAL)へ収束する
    fluctuation_sigma = max(0.01, 1.0 - (base_depth / 10.0))
    
    # ガウス分布による実効ゲインの揺れ幅シミュレーション（試行回数: 5回）
    fluctuated_samples = [
        random.gauss(base_gain, fluctuation_sigma) for _ in range(5)
    ]
    
    avg_gain = sum(fluctuated_samples) / len(fluctuated_samples)

    # 2. 確率的なREAL判定（固定の閾値ではなく、ゆらぎを含めた確率出力）
    # モードが EXTREME の場合、実効ゲインに応じたREAL確率を算出
    if mode == "EXTREME":
        real_probability = 1.0 / (1.0 + math.exp(-(avg_gain - 2.5) * 2))
    else:
        real_probability = 0.1 * (avg_gain / 5.0)

    # 0.0 ~ 1.0 の確率判定
    is_real = real_probability > 0.5

    return {
        "loaded_definition": user_def,
        "fluctuation_metrics": {
            "fluctuation_sigma (揺れ幅の大きさ)": round(fluctuation_sigma, 4),
            "sampled_gains (5回の揺らぎ試行値)": [round(x, 4) for x in fluctuated_samples],
            "average_gain (実効平均ゲイン)": round(avg_gain, 4)
        },
        "audit_result": "REAL_MODE" if is_real else "FAKE_OR_STANDARD_MODE",
        "real_probability (REAL成立確率)": f"{round(real_probability * 100, 2)}%",
        "note": "ゆらぎ（揺れ幅）を含む動的確率評価結果です。"
    }

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "my_def.json"
    res = audit_with_fluctuation(filepath)
    print("\033[1;36m[DYNAMIC AUDIT LOG]\033[0m")
    print(json.dumps(res, indent=2, ensure_ascii=False))
