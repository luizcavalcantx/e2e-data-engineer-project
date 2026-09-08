# Rebuild the pipeline images and drop the now-dangling (<none>) leftovers.
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

docker build -t crypto-extract:latest ./extract
docker build -t crypto-dbt:latest ./crypto_pipeline

# Removes ALL dangling images on the host (untagged, usually safe).
docker image prune -f
