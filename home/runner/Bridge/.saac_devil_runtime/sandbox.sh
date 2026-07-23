#!/usr/bin/env bash
set -euo pipefail

# Subshell isolation wrapper
(
  export PATH="/usr/local/bin:/usr/bin:/bin"
  exec "$@"
)
