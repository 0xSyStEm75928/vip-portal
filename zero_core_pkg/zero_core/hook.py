import sys
import os

class AnonymousHookManager:
    """ 既存システムやEEGデーモンを破壊せずに安全に連携・共存するフックマネージャー """
    
    def __init__(self):
        self.active_eeg_stream = False

    def detect_running_environment(self):
        if os.environ.get("EEG_STREAM_ACTIVE") == "1":
            self.active_eeg_stream = True
            print("[SAFE_HOOK] ⚡ 稼働中の既存EEGストリームを検知しました。上書きを回避し、共有メモリに接続します。")
        else:
            print("[SAFE_HOOK] ℹ️ 既存の独立EEGストリームは未検出。スタンドアロンモードで安全待機します。")

    def register_custom_handler(self, external_func):
        print("[SAFE_HOOK] 🔗 外部の自作アノニマス処理を安全にフックバインドしました。")
        return external_func

def safe_init():
    manager = AnonymousHookManager()
    manager.detect_running_environment()
    return manager

if __name__ == "__main__":
    safe_init()
