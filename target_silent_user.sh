#!/bin/bash

TARGET_FILE="index.html"
NOW_TIME=$(date -u +"%Y-%m-%d %H:%M:%S")

echo "[INFO] Re-targeting ONLY invisibleuser321 for Silent View..."

python3 -c "
import json, re

target = '$TARGET_FILE'
with open(target, 'r') as f:
    content = f.read()

match = re.search(r'<pre id=\"manifest-data\">(.*?)</pre>', content, re.DOTALL)
if match:
    data = json.loads(match.group(1).strip())
    
    # 公開顧客をすべて除去し、invisibleuser321 のみをサイレントターゲットに固定
    data['silent_target'] = {
        'github_id': 'invisibleuser321',
        'display_name': 'Capt. Chaos',
        'target_type': 'EXPLICIT_SILENT_VIEWER',
        'score_holding': '98.8%',
        'status': 'ANCHORED_IN_BACKGROUND'
    }
    
    # 他の一般フォロワーデータは破棄・クリア
    if 'verified_followers_mapped' in data:
        del data['verified_followers_mapped']
        
    data['counterparty_identity'] = {
        'bound_github_id': 'invisibleuser321',
        'mode': 'SILENT_LOCK'
    }
    
    data['timestamp'] = '$NOW_TIME'
    
    formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
    
    new_content = re.sub(
        r'<pre id=\"manifest-data\">.*?</pre>',
        f'<pre id=\"manifest-data\">\n{formatted_json}\n</pre>',
        content,
        flags=re.DOTALL
    )
    
    with open(target, 'w') as f:
        f.write(new_content)
        
    print('[SUCCESS] Targeted ONLY invisibleuser321. Public accounts removed.')
    print(formatted_json)
else:
    print('[FAIL] Manifest block not found.')
"

