import getpass
import json
import urllib.request
from web3 import Web3

# Polygon RPC
w3 = Web3(Web3.HTTPProvider("https://polygon-rpc.com"))

print("=== Keysmith Safe Direct Deployer ===")
# 画面に文字を出さずに秘密鍵を入力（履歴に残りません）
pk = getpass.getpass(prompt="秘密鍵を入力してください (画面には表示されません): ").strip()

if not pk.startswith("0x"):
    pk = "0x" + pk

try:
    account = w3.eth.account.from_key(pk)
    print(f"デプロイ元アドレス: {account.address}")

    # KeysmithLicense のバイナリデータ
    bytecode = "0x608060405234801561001057600080fd5b336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff02191646179055506102aa806100436000396000f3fe6080604052"

    tx = {
        'nonce': w3.eth.get_transaction_count(account.address),
        'gasPrice': w3.eth.gas_price,
        'gas': 300000,
        'data': bytecode,
        'chainId': 137 # Polygon
    }

    print("宛先(To)なしのデプロイTxを作成＆送信中...")
    signed_tx = w3.eth.account.sign_transaction(tx, pk)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("\n==========================================")
    print(f"[SUCCESS] コントラクトデプロイ命令を送信しました！")
    print(f"TX Hash: {tx_hash.hex()}")
    print("==========================================")

except Exception as e:
    print(f"\n[ERROR] デプロイ失敗: {e}")

