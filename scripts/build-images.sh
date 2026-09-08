#!/usr/bin/env bash
# Rebuild the pipeline images and drop the now-dangling (<none>) leftovers.
set -euo pipefail

cd "$(dirname "$0")/.."

docker build -t crypto-extract:latest ./extract
docker build -t crypto-dbt:latest ./crypto_pipeline

# Removes ALL dangling images on the host (untagged, usually safe).
docker image prune -f
