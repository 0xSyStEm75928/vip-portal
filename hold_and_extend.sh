#!/bin/bash

TARGET_FILE="index.html"
NOW_TIME=$(date -u +"%Y-%m-%d %H:%M:%S")

echo "[INFO] Applying 100% Hold & Sequence Extension..."

python3 -c "
import json, re

target = '$TARGET_FILE'
with open(target, 'r') as f:
    content = f.read()

match = re.search(r'<pre id=\"manifest-data\">(.*?)</pre>', content, re.DOTALL)
if match:
    data = json.loads(match.group(1).strip())
    
    # こちら側を 100.0% に引き上げ、相手側は維持
    data['score']['my_score'] = '100.0%'
    data['score']['counterparty_score'] = '98.8%'
    
    # ステータスを引き伸ばし・待機固定へシフト
    data['status'] = 'AWAITING_COUNTERPARTY_ACTION_EXTENDED'
    data['timestamp'] = '$NOW_TIME'
    
    # 引き伸ばし・サムシングエルスコース用の拡張パラメータ
    data['sequence_control'] = {
        'hold_state': True,
        'extension_applied': True,
        'something_else_route_available': True,
        'timeout_mode': 'SUSPENDED_UNTIL_SYNC'
    }
    
    formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
    
    new_content = re.sub(
        r'<pre id=\"manifest-data\">.*?</pre>',
        f'<pre id=\"manifest-data\">\n{formatted_json}\n</pre>',
        content,
        flags=re.DOTALL
    )
    
    with open(target, 'w') as f:
        f.write(new_content)
        
    print('[SUCCESS] State updated to 100% Hold. Counterparty locked at 98.8%.')
    print(formatted_json)
else:
    print('[FAIL] Manifest block not found.')
"

