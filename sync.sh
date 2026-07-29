#!/bin/sh
TARGET="${1:-CUSTOMER_001}"
PCT="${2:-100}"
python3 sync_pipeline.py "$TARGET" "$PCT"
