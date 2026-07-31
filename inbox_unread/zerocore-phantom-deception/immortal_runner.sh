#!/bin/bash

# Ctrl+C (SIGINT) や 終了シグナル (SIGTERM) を無視（無効化）する
trap 'echo " ⚠️ [TRAP TRIGGERED] Ctrl+C / Stop Signal Ignored by Phantom Engine. You cannot escape.";' INT TERM

echo "=================================================="
echo " 🌀 ZeroCore Immortal Deception Wrapper (Bash Layer)"
echo "=================================================="

# 無限ループで Python のポイズン罠を監視・自動復帰
while true; do
    python3 deception_runner.py
    
    # Python が何らかの理由で強制終了した場合のログ
    echo " 🔄 [REBOOT] Python process was interrupted/stopped. Respawning Phantom State immediately..."
    sleep 1
done
