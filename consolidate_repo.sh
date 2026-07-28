#!/usr/bin/env bash
set -euo pipefail

echo "======================================================================"
echo "    ZEROCORE REPOSITORY CONSOLIDATION (極限凝縮 ＆ 整理)              "
echo "======================================================================"

# 0. 退避用バックアップディレクトリの作成
mkdir -p ./backup_archive

# 1. covert_signal_001〜100 を 1つのマスターJSONに凝縮
echo "[1/3] Consolidating 100 covert_signal files into zerocore.master.signals.json ..."
find . -maxdepth 2 -name "covert_signal_*.json" | sort | xargs jq -s '{
  master_signals_version: "1.0.0",
  total_signals: length,
  signals: .
}' > zerocore.master.signals.json

# バックアップへ退避
find . -maxdepth 2 -name "covert_signal_*.json" -exec mv {} ./backup_archive/ \;
echo "  -> 100 files merged into zerocore.master.signals.json 🟢"

# 2. sovereign_part1〜5 を 1つのマスターJSONに凝縮
echo "[2/3] Consolidating sovereign_part files into zerocore.master.sovereign.json ..."
find . -maxdepth 2 -name "sovereign_part*.json" | sort | xargs jq -s '{
  master_sovereign_version: "1.0.0",
  parts_count: length,
  sovereign_modules: .
}' > zerocore.master.sovereign.json

# バックアップへ退避
find . -maxdepth 2 -name "sovereign_part*.json" -exec mv {} ./backup_archive/ \;
echo "  -> Sovereign parts merged into zerocore.master.sovereign.json 🟢"

# 3. proof_of_concept_v1〜v5 を 1つのマスターJSONに凝縮
echo "[3/3] Consolidating proof_of_concept files into zerocore.master.poc.json ..."
find . -maxdepth 2 -name "proof_of_concept*.json" | sort | xargs jq -s '{
  master_poc_version: "1.0.0",
  poc_count: length,
  proofs: .
}' > zerocore.master.poc.json

# バックアップへ退避
find . -maxdepth 2 -name "proof_of_concept*.json" -exec mv {} ./backup_archive/ \;
echo "  -> Proof of Concept files merged into zerocore.master.poc.json 🟢"

echo "----------------------------------------------------------------------"
echo " SUCCESS: 110+ scattered files condensed into 3 Master Records!"
echo " Original files are safely preserved in ./backup_archive/"
echo "======================================================================"
