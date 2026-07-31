#!/bin/bash

MY_GITHUB_ID="0xSyStEm75928"
TARGET_ID="invisibleuser321"

PRE_FILE="manifest_pre_fit.json"
POST_FILE="manifest_post_fit_RESULT.json"

echo "[INFO] Running actual API fit check against $TARGET_ID..."

# APIによるフォロー関係のステータスコード取得 (204: 成功, 404: 不成立)
FOLLOWING_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://api.github.com/users/$MY_GITHUB_ID/following/$TARGET_ID")
FOLLOWER_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://api.github.com/users/$TARGET_ID/following/$MY_GITHUB_ID")

python3 -c "
import json

with open('$PRE_FILE', 'r') as f:
    data = json.load(f)

is_following = ('$FOLLOWING_STATUS' == '204')
is_follower = ('$FOLLOWER_STATUS' == '204')

# 適合判定（ファクトのみ）
data['phase'] = 'POST_FIT_VERIFIED'
data['actual_fit_check'] = {
    'my_following_target': is_following,
    'target_following_me': is_follower,
    'http_codes': {
        'my_request': '$FOLLOWING_STATUS',
        'target_request': '$FOLLOWER_STATUS'
    }
}

if is_following and is_follower:
    data['fit_status'] = 'MATCH_CONFIRMED'
    data['verification_required']['github_api_verified'] = True
else:
    data['fit_status'] = 'MISMATCH_OR_PENDING'
    data['verification_required']['github_api_verified'] = False

with open('$POST_FILE', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('[SUCCESS] Post-fit verification file created: $POST_FILE')
"

