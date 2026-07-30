import sys
from pylsl import StreamInlet, resolve_byprop

def main():
    print("EEGストリームを検索中...")
    # LSLネットワークから 'type' が 'EEG' のストリームを探す
    streams = resolve_byprop('type', 'EEG', timeout=5.0)

    if not streams:
        print("エラー: 有効なEEGデバイス/ストリームが見つかりませんでした。")
        print("デバイスがPCに接続され、LSL配信ソフトが起動しているか確認してください。")
        sys.exit(1)

    print(f"ストリームを発見しました: {streams[0].name()}")
    inlet = StreamInlet(streams[0])

    print("--- 脳波データ受信開始 (Ctrl+C で終了) ---")
    try:
        while True:
            # 脳波データ（サンプル）とタイムスタンプを取得
            sample, timestamp = inlet.pull_sample()
            
            # ターミナルへリアルタイム出力（先頭4チャンネルを表示する例）
            channels_str = " | ".join([f"Ch{i+1}: {val:8.2f} µV" for i, val in enumerate(sample[:4])])
            print(f"[{timestamp:.3f}] {channels_str}", end="\r")

    except KeyboardInterrupt:
        print("\n受信を停止しました。")

if __name__ == "__main__":
    main()
