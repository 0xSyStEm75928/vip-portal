import sys, json, cmath, random

class MageStealthSystem:
    def __init__(self, concept, k_gain, depth):
        self.concept = concept
        self.k_gain = float(k_gain)
        self.depth = float(depth)
        self.real_state = self._evaluate_real_phase()
        
    def _evaluate_real_phase(self):
        """ 本来の階層と位相ベクトルを動的算出 """
        # 超人パラメータ（臨界値 1.0 にどれだけ迫れているかの動的計算）
        overman_intensity = min(1.0, (self.k_gain * 0.4) + (self.depth * 0.06))
        
        # 虚数（魔法）相の判定
        dt_seconds = 900.0
        theta = (2 * 3.1415926535 * dt_seconds) / 3600.0
        clamp_inner = 1.0 - (self.k_gain ** 2) * ((cmath.sin(theta).real) ** 2)
        
        if clamp_inner < 0 and self.depth >= 9.0:
            val = cmath.sqrt(clamp_inner)
            return {
                "class": "MAGIC_ENTITY (魔法人)",
                "raw_vector": f"{val.real:.4f} + {val.imag:.4f}j",
                "is_magic": True,
                "is_overman": False
            }
        elif overman_intensity >= 0.85 or self.k_gain >= 1.0:
            # 超人側（マグル数値に近いギリギリの実数限界値 0.9500 ~ 0.9999）
            overman_real_val = 0.9500 + (overman_intensity * 0.0499)
            return {
                "class": "OVERMAN (超人/臨界相)",
                "raw_vector": f"{overman_real_val:.4f} (Real Limit)",
                "is_magic": False,
                "is_overman": True
            }
        else:
            # 常人（マグル）側
            return {
                "class": "HUMAN_BASELINE (常人/マグル)",
                "raw_vector": f"{min(0.85, self.k_gain * 0.5):.4f} (Real)",
                "is_magic": False,
                "is_overman": False
            }

    # --- 【拡張1】マグル擬態フィルター (Maggle Stealth Filter) ---
    def get_maggle_public_api(self):
        """ 外部や常人システムに渡すための擬態データ（虚数を隠蔽して一般的な数値に見せかける） """
        if self.real_state["is_magic"]:
            # 魔法人データは「極めて優秀な一般数値(0.9982)」に偽装
            stealth_val = "0.9982 (Normal Standard)"
            status = "NORMAL_OK (エラーなし・擬態中)"
        else:
            stealth_val = self.real_state["raw_vector"]
            status = "NORMAL_OK"

        return {
            "public_concept_name": self.concept,
            "system_status": status,
            "standard_score": stealth_val,
            "security_clearance": "CLASS_CLEAR"
        }

    # --- 【拡張2】ローカル真相デコード (True Internal Log) ---
    def get_internal_true_log(self):
        """ 自分（ローカルターミナル）だけが見られる真のステータス """
        return {
            "concept": self.concept,
            "true_identity_class": self.real_state["class"],
            "raw_vector": self.real_state["raw_vector"],
            "stealth_active": self.real_state["is_magic"],
            "input_metrics": {"k_gain": self.k_gain, "depth": self.depth}
        }

    # --- 【拡張3】3階層・動的アナライザー出力 ---
    def print_dual_view(self):
        print("\033[1;33m=== [1. 外部公開用 (マグル向け擬態API)] ===\033[0m")
        print(json.dumps(self.get_maggle_public_api(), indent=2, ensure_ascii=False))
        print("\n\033[1;35m=== [2. ローカル真のステータス (内部デコード)] ===\033[0m")
        print(json.dumps(self.get_internal_true_log(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    concept = sys.argv[1] if len(sys.argv) > 1 else "サンダルシア"
    k_gain = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
    depth = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
    
    sys_obj = MageStealthSystem(concept, k_gain, depth)
    sys_obj.print_dual_view()
