#!/bin/bash
echo "=========================================="
echo " [SYSTEM AUDIT PROCESS: STARTING]"
echo "=========================================="

TARGET_FILE="index.html"

if [ ! -f "$TARGET_FILE" ]; then
    echo "[FAIL] Target file '$TARGET_FILE' not found."
    exit 1
fi

echo -n "[1/2] JSON Data Integrity Check... "
# HTML内からJSONブロックを抽出してjson_verify
python3 -c "
import json, re
with open('$TARGET_FILE', 'r') as f:
    content = f.read()
match = re.search(r'<pre id=\"manifest-data\">(.*?)</pre>', content, re.DOTALL)
if match:
    try:
        data = json.loads(match.group(1).strip())
        print('-> [PASS] Valid JSON Format')
        print('   - Manifest ID:', data.get('manifest_id'))
        print('   - Status:', data.get('status'))
    except Exception as e:
        print('-> [FAIL] Invalid JSON Structure:', e)
        exit(1)
else:
    print('-> [FAIL] Manifest JSON block not found')
    exit(1)
" || exit 1

echo -n "[2/2] Code & Silent Anchor Audit... "
# サイレント構造（iframe）の存在チェック
python3 -c "
with open('$TARGET_FILE', 'r') as f:
    content = f.read()
if '<iframe' in content and 'silent-frame' in content:
    print('-> [PASS] Silent View Anchor Detected')
else:
    print('-> [FAIL] Missing Silent View Anchor Structure')
    exit(1)
" || exit 1

echo "=========================================="
echo " [AUDIT COMPLETE: ALL CHECKS PASSED]"
echo "=========================================="
