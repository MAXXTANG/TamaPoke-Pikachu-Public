#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLI=(arduino-cli)
if [[ $# -gt 0 ]]; then
  if [[ $# -ne 2 || "$1" != "--config-file" ]]; then
    echo "Usage: bash tools/build.sh [--config-file PATH]" >&2
    exit 2
  fi
  CLI+=(--config-file "$2")
fi

python3 "$REPO_DIR/tools/generate_embedded.py" --check
"${CLI[@]}" compile --warnings=all --jobs 4 \
  --fqbn 'esp32:esp32:esp32s3:CDCOnBoot=cdc,FlashSize=16M,PSRAM=opi,PartitionScheme=app3M_fat9M_16MB' \
  --build-path "$REPO_DIR/build/arduino" \
  --output-dir "$REPO_DIR/build/output" \
  "$REPO_DIR/TamaPoke"
