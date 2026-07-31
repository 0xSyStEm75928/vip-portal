#!/bin/bash

# あなたのGitHubアカウントID（※適宜変更してください）
MY_GITHUB_ID="0xSyStEm75928"
TARGET_ID="invisibleuser321"
TARGET_FILE="index.html"

echo "[API CHECK] Checking follow state between $MY_GITHUB_ID and $TARGET_ID..."

# GitHub APIで相互フォロー状態を物理取得
FOLLOWING_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://api.github.com/users/$MY_GITHUB_ID/following/$TARGET_ID")
FOLLOWER_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://api.github.com/users/$TARGET_ID/following/$MY_GITHUB_ID")

python3 -c "
import json, re, sys

my_id = '$MY_GITHUB_ID'
target_id = '$TARGET_ID'
following_code = '$FOLLOWING_STATUS'
follower_code = '$FOLLOWER_STATUS'

# 204: フォロー中 / 404: 未フォロー
is_following = (following_code == '204')
is_follower = (follower_code == '204')

print(f'[RAW DATA] Following ({my_id} -> {target_id}): {is_following} ({following_code})')
print(f'[RAW DATA] Followed by ({target_id} -> {my_id}): {is_follower} ({follower_code})')

# 適合判定（APIレスポンスの事実のみ）
if is_following and is_follower:
    fit_result = 'MUTUAL_FOLLOW_CONFIRMED'
    fit_boolean = True
elif is_following or is_follower:
    fit_result = 'ONE_WAY_FOLLOW_DETECTED'
    fit_boolean = False
else:
    fit_result = 'NO_FOLLOW_RELATION'
    fit_boolean = False

target_file = '$TARGET_FILE'
with open(target_file, 'r') as f:
    content = f.read()

match = re.search(r'<pre id=\"manifest-data\">(.*?)</pre>', content, re.DOTALL)
if match:
    data = json.loads(match.group(1).strip())
    
    # 物理確認結果をそのまま上書き反映
    data['verification_required']['github_api_verified'] = fit_boolean
    data['actual_fit_check'] = {
        'target_id': target_id,
        'my_following': is_following,
        'target_following_me': is_follower,
        'fit_result': fit_result
    }

    formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
    new_content = re.sub(r'<pre id=\"manifest-data\">.*?</pre>', f'<pre id=\"manifest-data\">\n{formatted_json}\n</pre>', content, flags=re.DOTALL)
    
    with open(target_file, 'w') as f:
        f.write(new_content)
        
    print('[SUCCESS] Manifest updated with raw API verification data.')
else:
    print('[FAIL] Manifest block not found.')
"
