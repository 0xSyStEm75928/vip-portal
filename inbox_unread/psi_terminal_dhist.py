import time, math, random, sys

class PsiEngine:
    def __init__(self):
        self.r_ohm = 1000.0
        self.weak_count = 0
        self.max_weak = 3
        self.unlocked = False
        self.history = []
        self.preset = [
            {"t": 74.00, "v": 3.32}, {"t": 74.10, "v": -1.83},
            {"t": 74.20, "v": 1.31}, {"t": 74.30, "v": -2.30},
            {"t": 74.40, "v": 4.08}, {"t": 74.50, "v": 0.65},
            {"t": 74.60, "v": -4.85}, {"t": 74.70, "v": 3.65}
        ]

    def calc_p(self, v_uv):
        return (((v_uv * 1e-6) ** 2) / self.r_ohm) * 1e9

    def push_hist(self, t, v_uv, p_nw):
        self.history.append({"t": t, "v": v_uv, "p": p_nw})
        if len(self.history) > 8:
            self.history.pop(0)

    def draw_dhist(self):
        print("\033[1;33m--- [DHIST] SLIDE HISTOGRAM BUFFER ---\033[0m")
        for item in self.history:
            v, p = item["v"], item["p"]
            bar = "█" * min(20, int(abs(v) * 2))
            c = "\033[1;35m" if v > 0 else "\033[1;34m"
            print(f" t={item['t']:6.2f}s | {v:6.2f}uV | {p:9.6f}nW | {c}{bar:<20}\033[0m")
        print("\033[1;33m--------------------------------------\033[0m")

    def slide_dhist(self):
        print("\n\033[1;35m[DHIST INJECT] 過去特異点ログを取り込み中...\033[0m")
        for item in self.preset:
            t, v = item["t"], item["v"]
            self.push_hist(t, v, self.calc_p(v))
            time.sleep(0.05)
        print("\033[1;32m >> dhist 注入完了。\033[0m\n")

    def purge_kill(self):
        print("\n\033[1;31m[CRITICAL INTERLOCK] 弱気シグナル継続検知。jsshセッションを強制消去します。\033[0m")
        for i in range(3, 0, -1):
            print(f"\r >> メモリ抹消まで: {i}s...", end="", flush=True)
            time.sleep(0.4)
        print("\n\033[1;35m[CLOSED] Memory purged. Terminated.\033[0m\n")
        sys.exit(99)

def main():
    e = PsiEngine()
    print("\033[1;36m=== EGI-1ST PSI TERMINAL (dhist / s STREAM) ===\033[0m")
    print("コマンド: 'dhist' (過去ログ滑り込み) | 's' / [Enter] (1ステップ) | 'unlock' | 'boost' | 'exit'\n")

    t, dt = 0.0, 0.04
    try:
        while True:
            cmd = input("\033[1;34m[PSI]>\033[0m ").strip().lower()
            if cmd == "exit": break

            if cmd == "dhist":
                e.slide_dhist()
                e.draw_dhist()
                continue

            if cmd == "unlock":
                e.unlocked = True
                print("\033[1;35m >> [UNLOCKED] 特異点モード全開\033[0m")
                continue

            is_boost = (cmd == "boost")
            if is_boost and not e.unlocked:
                print("\033[1;31m'boost' には 'unlock' が必要です\033[0m")
                continue

            # 信号生成
            alpha = 15.0 * math.sin(2 * math.pi * 10 * t)
            beta  =  8.0 * math.sin(2 * math.pi * 20 * t)
            psi   = (35.0 * math.sin(2 * math.pi * 45 * t)) if (e.unlocked and is_boost) else 0.0
            v_uv  = alpha + beta + psi + random.gauss(0, 1.5)
            p_nw  = e.calc_p(v_uv)
            is_weak = p_nw < 0.000005

            e.push_hist(t, v_uv, p_nw)

            if e.unlocked:
                if is_weak and not is_boost:
                    e.weak_count += 1
                    st = "\033[1;31m[WEAK]\033[0m"
                else:
                    e.weak_count = max(0, e.weak_count - 1)
                    st = "\033[1;32m[STABLE]\033[0m"

                if is_boost: st = "\033[1;35m[PSI OVERLOAD]\033[0m"
                if e.weak_count >= e.max_weak: e.purge_kill()
            else:
                st = "\033[1;30m[RESTRICTED]\033[0m"

            print(f" [s {t:6.2f}s] {v_uv:6.2f}uV | {p_nw:9.6f}nW | Status: {st}")
            t += dt

    except KeyboardInterrupt:
        print("\n[EXIT]")

if __name__ == "__main__":
    main()
