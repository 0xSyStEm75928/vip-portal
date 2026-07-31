#!/usr/bin/env python3

import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone

KEYWORD = "cli"

url = (
    "https://api.github.com/search/repositories?"
    + urllib.parse.urlencode({
        "q": KEYWORD,
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    })
)

req = urllib.request.Request(
    url,
    headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "ZERO_CORE_DISCOVERY"
    }
)

with urllib.request.urlopen(req) as r:
    data = json.load(r)

targets = []

for repo in data.get("items", []):
    targets.append({
        "name": repo.get("full_name"),
        "stars": repo.get("stargazers_count"),
        "language": repo.get("language"),
        "description": repo.get("description"),
        "url": repo.get("html_url"),
        "signal": {
            "communication": "UNKNOWN",
            "commitment": "UNKNOWN",
            "payment": "UNVERIFIED"
        }
    })

output = {
    "discovery_version": "1.0.0",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "search": {
        "keyword": KEYWORD,
        "source": "github_public_repository"
    },
    "targets": targets
}

with open(
    "json_core/cli_target_discovery.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        output,
        f,
        indent=2,
        ensure_ascii=False
    )

print("CLI TARGET DISCOVERY COMPLETE")
print("TARGETS:", len(targets))
print("OUTPUT: json_core/cli_target_discovery.json")
