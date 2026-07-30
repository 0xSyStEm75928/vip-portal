import sys, json, cmath

def evaluate_element(concept_name, raw_k_gain, observation_depth):
    """
    ユーザーからのエレメント入力パラメータ（k_gain, observation_depth）に基づいて
    位相計算を行い、魔法人フラグを測定・出力するスクリプト
    """
    
    # 1. k_gain から位相・ベクトル（実数 vs 虚数）を計算
    # (dt_seconds=900.0s 相当の位相移動を固定適用)
    dt_seconds = 900.0
    theta = (2 * 3.1415926535 * dt_seconds) / 3600.0
    clamp_inner = 1.0 - (raw_k_gain ** 2) * ((cmath.sin(theta).real) ** 2)
    
    if clamp_inner < 0:
        val = cmath.sqrt(clamp_inner)
        vector_str = f"{val.real:.4f} + {val.imag:.4f}j"
        has_complex = True
    else:
        vector_str = f"{cmath.sqrt(clamp_inner).real:.4f} (Real)"
        has_complex = False

    # 2. 条件チェック
    is_deep = observation_depth >= 9.0
    has_density = len(concept_name.encode('utf-8')) / (len(concept_name) + 1e-5) >= 1.5

    conditions = {
        "has_complex_phase (虚数位相)": has_complex,
        "deep_observation (極限観測)": is_deep,
        "structural_density (構造密度)": has_density
    }

    # 3. クラス判定
    satisfied = sum(conditions.values())
    if satisfied == 3:
        evaluated_class = "MAGIC_ENTITY (魔法人相 / 構造再構成)"
        verified = True
        msg = "【完全適合】エレメントパワーは閾値を突破し、虚数相へ相転移しました。"
    elif has_complex or is_deep:
        evaluated_class = "OVERMAN (超人相 / 臨界領域)"
        verified = False
        msg = "【臨界領域】強いエレメントを検出しましたが、全条件到達には至っていません。"
    else:
        evaluated_class = "HUMAN_BASELINE (常人相 / 標準実数)"
        verified = False
        msg = "【標準実数】エレメント数値が標準領域に留まっています。"

    return {
        "concept": concept_name,
        "input_element_power": {
            "k_gain": raw_k_gain,
            "observation_depth": observation_depth
        },
        "calculated_vector": vector_str,
        "evaluated_class": evaluated_class,
        "is_magic_entity_verified": verified,
        "condition_checks": conditions,
        "analysis_output": msg
    }

if __name__ == "__main__":
    # 引数取得: python3 magic_entity_analyzer.py <概念名> <k_gain> <観測深度>
    concept = sys.argv[1] if len(sys.argv) > 1 else "サンダルシア"
    k_gain = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
    depth = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0

    res = evaluate_element(concept, k_gain, depth)
    print("\033[1;35m[ELEMENT ANALYZER LOG]\033[0m")
    print(json.dumps(res, indent=2, ensure_ascii=False))
