import os, sys, json, subprocess
from pipeline_master import MasterPipeline

def copy_to_clipboard(text):
    """ APIを使わず、ローカルのクリップボードへデータを送り込む """
    try:
        # Linux / Termux (termux-clipboard-set / xclip / xsel)
        if os.system("type termux-clipboard-set > /dev/null 2>&1") == 0:
            p = subprocess.Popen(['termux-clipboard-set'], stdin=subprocess.PIPE)
            p.communicate(input=text.encode('utf-8'))
            return True
        elif os.system("type xclip > /dev/null 2>&1") == 0:
            p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            p.communicate(input=text.encode('utf-8'))
            return True
        elif os.system("type pbcopy > /dev/null 2>&1") == 0: # Mac
            p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            p.communicate(input=text.encode('utf-8'))
            return True
    except Exception:
        pass
    return False

def auto_packet_export(user_input):
    # 1. ローカル側でデータ構造化（メタデータ・過去文脈の解析）
    packet = MasterPipeline.execute(user_input)
    
    tone = packet["meta_analysis"]["declared_tone"]
    context_count = packet["inherited_context_count"]
    payload_hash = packet["telemetry"]["payload_hash"]

    # 2. APIを使わずにGeminiへ渡す「完全構造化プロンプトパケット」の構築
    formatted_packet = f"""【NON-API PIPELINE PACKET】
[System Metadata] Tone={tone} | Context_Inherited={context_count} | Hash={payload_hash}
[User Input] {user_input}

---
※上記のメタデータと文脈を反映して回答してください。"""

    # 3. クリップボードへコピー
    copied = copy_to_clipboard(formatted_packet)

    print("\n\033[1;32m[NON-API PACKET READY]\033[0m")
    if copied:
        print("\033[1;36m[クリップボードに自動コピーされました！]\033[0m")
        print("チャット欄にペースト (Ctrl+V) して送信してください。\n")
    else:
        print("\033[1;33m[以下のテキストをコピーしてチャット欄に貼り付けてください]\033[0m\n")
        print(formatted_packet)

if __name__ == "__main__":
    inp = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "ノンAPI連携テスト"
    auto_packet_export(inp)
