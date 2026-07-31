#!/bin/bash

TARGET_FILE="index.html"
NEW_TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S")

# 1. 引数から新しい状態や新規クライアント名を取得（デフォルト設定あり）
NEW_STATUS="${1:-RECONCILIATION_COMPLETED_PENDING_RELEASE}"
CLIENT_ID="${2:-CLIENT-NEW-002}"

echo "[INFO] Updating Manifest JSON with Silent Stream (-s)..."

# 2. JSON構造をサイレント生成・更新
python3 -c "
import json, re

target = '$TARGET_FILE'
with open(target, 'r') as f:
    content = f.read()

# JSON部分の抽出
match = re.search(r'<pre id=\"manifest-data\">(.*?)</pre>', content, re.DOTALL)
if match:
    data = json.loads(match.group(1).strip())
    
    # 既存データの更新 & 新規クライアント用フィールドの追加
    data['timestamp'] = '$NEW_TIMESTAMP'
    data['status'] = '$NEW_STATUS'
    data['active_client'] = '$CLIENT_ID'
    data['queue_status'] = 'READY_FOR_NEXT_TRANSACTION'
    
    # フォーマット整形
    updated_json = json.dumps(data, indent=2, ensure_ascii=False)
    
    # HTML内のJSONエリア置換
    new_content = re.sub(
        r'<pre id=\"manifest-data\">.*?</pre>',
        f'<pre id=\"manifest-data\">\n{updated_json}\n</pre>',
        content,
        flags=re.DOTALL
    )
    
    with open(target, 'w') as f:
        f.write(new_content)
        
    print('[PASS] JSON Manifest updated silently.')
    print(updated_json)
else:
    print('[FAIL] Manifest block not found.')
"

