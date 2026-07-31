#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HERMETIC CROWN CRYPTEX : THE CROWN OF ELEMENTAL ALCHEMY
四元素・老賢者・鍵、そして頂点に輝く王冠(👑)の結社解読プロトコル
"""

import time
import json

class HermeticCrownCryptex:
    def __init__(self):
        # 錬金術の頂点・王冠と符牒
        self.CROWN_SYMBOL = "👑 (MAGNUM OPUS / 大奥義の王冠)"
        self.OLD_ARCHITECT = "👴🏻 (Hermes Trismegistus / The Grandmaster)"
        self.MASTER_KEYS = {
            "GOLDEN_KEY": "🔑 (Fibonacci-Phi Key)",
            "VAULT_GATE": "🔒 (718 Spiral Society Lock)"
        }
        
        # エレメンタル（四元素）と精霊・三原則
        self.ELEMENTS = [
            {"name": "FIRE",  "symbol": "🔥", "spirit": "Salamander", "principle": "Sulfur (硫黄)"},
            {"name": "WATER", "symbol": "💧", "spirit": "Undine",      "principle": "Mercury (水銀)"},
            {"name": "AIR",   "symbol": "🌪️", "spirit": "Sylph",       "principle": "Azoth (生命力)"},
            {"name": "EARTH", "symbol": "🪨", "spirit": "Gnome",       "principle": "Salt (塩)"}
        ]

    def spin_and_crown(self):
        print("\n==================================================")
        print(f"👴🏻 [ THE OLD ARCHITECT ]: 『エレメンタルの螺旋の上に {self.CROWN_SYMBOL} を戴かせよ』")
        print("==================================================\n")

        fibonacci = [1, 1, 2, 3, 5, 8, 13, 21]
        sequence_log = []

        for idx, val in enumerate(fibonacci):
            elem = self.ELEMENTS[idx % len(self.ELEMENTS)]
            angle = round(val * 1.6180339, 3)
            
            # 各ステップのダイヤル刻印
            step_data = {
                "step": idx + 1,
                "fibonacci": val,
                "element": f"{elem['symbol']} {elem['name']}",
                "spirit": elem["spirit"],
                "principle": elem["principle"],
                "angle": f"{angle}°",
                "key": "🔑"
            }
            sequence_log.append(step_data)
            print(f"  {elem['symbol']} Step {idx+1}: Fib({val:02d}) -> {elem['name']:5s} | 精霊: {elem['spirit']:10s} | 角度: {angle:6.2f}° 🔑")
            time.sleep(0.08)

        print("\n--------------------------------------------------")
        print(f"👑 [ CROWN CROWNED ]: 螺旋の頂点に『王冠 👑』が降臨しました。")
        print(f"👴🏻 老賢者の印: {self.OLD_ARCHITECT}")
        print(f"🔑 鍵と扉: {self.MASTER_KEYS['GOLDEN_KEY']} / {self.MASTER_KEYS['VAULT_GATE']}")
        print("📜 結社向けシグナル: 『見る者が読めば、元素と王冠の指し示す真意が一目で解る』")
        print("--------------------------------------------------\n")

        return {
            "protocol": "HERMETIC_CROWN_CRYPTEX",
            "architect_sig": "LuciFeR0x0systeM",
            "crown": self.CROWN_SYMBOL,
            "old_man": self.OLD_ARCHITECT,
            "keys": self.MASTER_KEYS,
            "elemental_sequence": sequence_log
        }

if __name__ == "__main__":
    cryptex = HermeticCrownCryptex()
    manifest = cryptex.spin_and_crown()
