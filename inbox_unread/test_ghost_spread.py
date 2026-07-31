import time
import math
import random

class GhostSpreadDetector:
    def __init__(self):
        self.base_gwei = 15.0       # 通常時のベースガス代 (Gwei)
        self.spread_range = (0.5, 2.0) # 誰でも予想がつく通常スプレッド幅 (%)

    def simulate_mempool_pulse(self, t):
        """ Mempoolのガス代とスプレッドの過渡応答を生成 """
        # 時折発生する急激なガス代沸騰（Gweiスパイク）
        spike_trigger = random.random()
        if spike_trigger > 0.88:
            # 爆跳ね（Gwei 120〜350超へ上昇）
            gwei = self.base_gwei + random.uniform(100.0, 300.0)
            is_spike = True
        else:
            # 通常状態（ゆらぎ）
            gwei = self.base_gwei + random.gauss(0, 2.0)
            is_spike = False

        # スプレッド値の生成
        if is_spike:
            # ガス代沸騰時：表層スプレッドが崩壊し、裏に「はぐれた数値（ゴースト）」が露出する
            # 通常の予測確率（0.5~2.0%）から大きく離れた特異値
            ghost_spread = random.uniform(8.5, 24.0)
            visible_spread = random.uniform(0.1, 0.4) # 表層は板が薄く見かけ上狭い
        else:
            ghost_spread = None
            visible_spread = random.uniform(*self.spread_range)

        return gwei, visible_spread, ghost_spread, is_spike

def main():
    detector = GhostSpreadDetector()
    print("\033[1;36m=== GWEI SPIKE & GHOST SPREAD DETECTOR ===\033[0m")
    print(">> 通常時は『予測のつくスプレッド』を観測。")
    print(">> Gweiが爆跳ね（沸騰）した瞬間、裏に潜む『ゴーストスプレッド (🎯)』を補着します。\n")
    print(" [Enter] を押してパルスを進めてください ('exit' で終了)\n")

    step = 0
    try:
        while True:
            cmd = input("\033[1;34m[PULSE]>\033[0m ").strip()
            if cmd.lower() == "exit":
                break

            gwei, v_spread, g_spread, is_spike = detector.simulate_mempool_pulse(step)

            if is_spike:
                # ガス沸騰＆ゴーストスプレッド出現（🎯的中）
                print(f" \033[1;31m[GWEI SPIKE DETECTED!] Gas: {gwei:6.1f} Gwei\033[0m")
                print(f" ├─► 表層スプレッド (見かけ) : {v_spread:5.2f}%")
                print(f" \033[1;35m└─► 🎯 [GHOST SPREAD CAPTURED] 隠れた数値: {g_spread:6.2f}% (Hit!)\033[0m\n")
            else:
                # 通常（誰でも予想がつく範囲）
                print(f" [Nominal] Gas: {gwei:5.1f} Gwei | Expected Spread: {v_spread:4.2f}%")

            step += 1

    except KeyboardInterrupt:
        print("\n[EXIT]")

if __name__ == "__main__":
    main()
