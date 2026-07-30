import time
import math
import statistics

class GhostSpreadMonitor:
    """
    通常時の安定板（Expected Spread）と、
    Gwei過渡スパイク時に露出する「ゴーストスプレッド（真空・歪み）」を
    評価・抽出する実用監視エンジン。
    """
    def __init__(self, spike_threshold_gwei=100.0, history_size=20):
        self.spike_threshold = spike_threshold_gwei
        self.history_size = history_size
        self.gwei_history = []
        
    def analyze_tick(self, current_gwei: float, visible_spread_pct: float) -> dict:
        """
        現在の Gwei と見かけのスプレッド（%）を受け取り、
        歪み・クリティカル（🎯）の発生有無を判定。
        """
        now = time.time()
        
        # 履歴バッファの更新
        self.gwei_history.append(current_gwei)
        if len(self.gwei_history) > self.history_size:
            self.gwei_history.pop(0)

        # 移動平均と移動標準偏差（ボラティリティ）の計算
        mean_gwei = statistics.mean(self.gwei_history) if self.gwei_history else current_gwei
        stdev_gwei = statistics.stdev(self.gwei_history) if len(self.gwei_history) > 1 else 0.0

        # Gwei急騰（スパイク）の検知: Z-Scoreまたは絶対閾値による評価
        is_spike = (current_gwei >= self.spike_threshold) or (
            stdev_gwei > 0 and (current_gwei - mean_gwei) / stdev_gwei > 3.0
        )

        critical_target = None
        if is_spike:
            # 圧力（Gweiスパイク）下で露出する真のスプレッド（真空領域）の理論推定
            # スパイクの度合いに応じて潜在スプレッドを導出
            pressure_factor = current_gwei / max(1.0, mean_gwei)
            critical_target = visible_spread_pct * (1.0 + math.log1p(pressure_factor) * 5.0)

        return {
            "timestamp": now,
            "current_gwei": current_gwei,
            "mean_gwei": mean_gwei,
            "visible_spread": visible_spread_pct,
            "is_critical": is_spike,
            "ghost_target": critical_target
        }

# --- 導入用サンプルコード ---
if __name__ == "__main__":
    monitor = GhostSpreadMonitor(spike_threshold_gwei=80.0)
    print("=== GHOST SPREAD ENGINE (NORMALIZED IMPLEMENTATION) ===")
    print(">> プロダクション導入用の監視モジュールが生成されました。")
    print(">> 実データ（Web3 API / RPCプロバイダ等）のTickを渡すことで即座に機能します。\n")

    # テストTickデータ（通常時 ──► スパイク時 ──► 収束時）
    test_ticks = [
        (15.2, 0.50),
        (16.1, 0.48),
        (14.8, 0.52),
        (120.5, 0.22), # 🎯 Gwei爆跳ね（クリティカル発生）
        (18.0, 0.45),
    ]

    for i, (gwei, spread) in enumerate(test_ticks, 1):
        res = monitor.analyze_tick(gwei, spread)
        if res["is_critical"]:
            print(f"[{i}] \033[1;35m[🎯 CRITICAL DETECTED]\033[0m Gas: {res['current_gwei']} Gwei | Visible: {res['visible_spread']}% | \033[1;36mGhost Target: {res['ghost_target']:.2f}%\033[0m")
        else:
            print(f"[{i}] [Nominal] Gas: {res['current_gwei']} Gwei | Visible: {res['visible_spread']}%")
