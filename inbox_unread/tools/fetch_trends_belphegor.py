import urllib.request
import xml.etree.ElementTree as ET
import json, time, os, hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_STORE = os.path.join(BASE_DIR, "data_store")
BELPHEGOR_STORE = os.path.join(DATA_STORE, "belphegor_stream.ndjson")

def fetch_latest_topics():
    # Googleニュース（主要トピック）のRSSフィードから最新ニュースを取得
    url = "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja"
    print("\033[1;36m[FETCHING]\033[0m 最新トレンド・トピックを自動吸い上げ中...")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        topics = []
        for item in root.findall('.//item')[:5]:  # 最新5件のトピックを抽出
            topics.append({
                "title": item.find('title').text if item.find('title') is not None else "",
                "link": item.find('link').text if item.find('link') is not None else "",
                "pubDate": item.find('pubDate').text if item.find('pubDate') is not None else ""
            })
        return topics
    except Exception as e:
        print(f"\033[1;31m[ERROR]\033[0m トレンド取得失敗: {e}")
        return []

def store_trend_belphegor():
    topics = fetch_latest_topics()
    if not topics:
        print("\033[1;33m[SKIP]\033[0m トピックの取得ができなかったため中断します。")
        return

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    belphegor_structure = {
        "$schema": "https://belphegor.dev/schemas/v1/belphegor-spec.json",
        "_belphegor_engine": {
            "entity": "BELPHEGOR_TREND_INVENTOR",
            "sloth_protocol": "AUTOMATED_TOPIC_LEVERAGE",
            "integrity_hash": "BEL-TREND-" + hashlib.sha256(now.encode()).hexdigest()[:12].upper(),
            "timestamp": now
        },
        "opponent_check": {
            "tactical_status": "TREND_ARMORED_MODE",
            "counter_measures": [
                "LATEST_INFORMATION_DISARM",
                "SILENT_404_TRAP_READY"
            ]
        },
        "payload_core": {
            "category": "REALTIME_TRENDS",
            "topic_count": len(topics),
            "topics": topics
        }
    }

    os.makedirs(DATA_STORE, exist_ok=True)
    with open(BELPHEGOR_STORE, "a", encoding="utf-8") as f:
        f.write(json.dumps(belphegor_structure, ensure_ascii=False) + "\n")

    print(f"\033[1;35m[TRENDS INJECTED]\033[0m {len(topics)} 件の最新トレンド・トピックを BelphegorJSON へ格納完了！")
    print(f"\033[1;32m[STORED]\033[0m `data_store/belphegor_stream.ndjson` へ配備完了。")

if __name__ == "__main__":
    store_trend_belphegor()
