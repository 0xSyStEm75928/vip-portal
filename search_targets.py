import urllib.request
import urllib.parse
import json

def find_active_targets(keyword="cli", min_stars=5, max_stars=300):
    query = f"{keyword} stars:{min_stars}..{max_stars} pushed:>2026-07-01 is:public"
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=updated&order=desc&per_page=5"

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            print(f"\n🎯 【公開ターゲット抽出結果】 Keyword: '{keyword}'\n" + "="*50)
            for repo in data.get("items", []):
                owner = repo["owner"]["login"]
                name = repo["name"]
                stars = repo["stargazers_count"]
                repo_url = repo["html_url"]
                print(f"👤 OWNER : {owner}")
                print(f"📦 REPO  : {name} (⭐ {stars})")
                print(f"🔗 URL   : {repo_url}")
                print("-" * 50)
    except Exception as e:
        print(f"❌ 取得エラー: {e}")

if __name__ == "__main__":
    find_active_targets()
