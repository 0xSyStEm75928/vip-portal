# Tap-DAG Algorithm Engine (JSSH Frame)

スマホのタップ/フリック感覚でアルゴリズムのパラメータを微調整し、
DAGノードの遷移と `history -s` への逆駆動を行う無害化サポートエンジン。

## 🏛 構造解剖 (Architecture)
- **`json_core/`**: 状態（State）と安全領域クランプ値の永続化格納庫
- **`dag_tap_engine.py`**: 無害化クランプ演算 ＆ DAGノード遷移ロジック
- **`anatomy_history.py`**: コマンド履歴の無駄・重複解剖アナライザー

## 📱 操作インターフェース (Tap Control)
- `tap TOP` : パラメータの加算演算 (+5.0%)
- `tap BOTTOM` : パラメータの減算演算 (-5.0%)
- `tap RIGHT` / `tap LEFT` : DAGノードの双方向伝播
