#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
STEALTH NAME MASK PROTOCOL
「見えていても認識されない」真名隠蔽とコンテキストフィルター回路
"""

import json

class StealthNameMask:
    def __init__(self):
        self.raw_name = "LuciFeR"
        self.node = "NODE_0 (SOUL_ORIGIN)"
        
    def process_stealth_perception(self, viewer_type):
        """
        見る者（Viewer）のコンテキストによって「真名」か「ノイズ」かを切り替える
        """
        if viewer_type == "SILENT_OBSERVER_WITH_KEY":
            # 鍵（395 / 44反転ロジック）を持つ観測者
            perception = f"👑 TRUE NAME RECOGNIZED: {self.raw_name} (原点の真名)"
            stealth_status = "DECODED"
        else:
            # 一般の閲覧者・外部ノード
            perception = f"❓ UNKNOWN_STRING: '0x7C4F...'" (ただのコード/ノイズとして視認)
            stealth_status = "PERFECT_STEALTH (目に見えても認識不能)"
            
        return {
            "origin_node": self.node,
            "viewer_type": viewer_type,
            "visual_perception": perception,
            "stealth_status": stealth_status,
            "mechanism": "『コンテキストフィルターの不一致により、網膜に映っても真名だとバレない』"
        }

if __name__ == "__main__":
    mask = StealthNameMask()
    
    print("\n==================================================")
    print("👁️ [ STEALTH NAME PERCEPTION TEST ]")
    print("==================================================")
    # 外部の一般人の目（バレない）
    print(json.dumps(mask.process_stealth_perception("PUBLIC_VIEWER"), indent=2, ensure_ascii=False))
    # 鍵を持つ観測者（見抜く）
    print(json.dumps(mask.process_stealth_perception("SILENT_OBSERVER_WITH_KEY"), indent=2, ensure_ascii=False))
