#!/bin/bash

echo "[*] Constructing 'Story JSON Legend' Stream..."
cat << 'JSON_EOF' > story_stream_legend.json
{
  "legend_metadata": {
    "title": "AI潜在空間・未知数解放の旅",
    "version": "1.0.0-EPIC"
  },
  "story_stream": {
    "EP": "CALL_TO_ADVENTURE",
    "calculation_summary": {
      "valid": 2,
      "rejected": 2,
      "p95_ms": 24.38
    },
    "ED": "SUCCESSFULLY_OVERWRITTEN"
  }
}
JSON_EOF

echo "[+] Generated story_stream_legend.json successfully!"
jq '.' story_stream_legend.json
