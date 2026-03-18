#!/usr/bin/env bash
set -e

cd /opt/apps/pdf-text-extractor

echo "==> Atualizando código"
git fetch origin
git reset --hard origin/main
git clean -fd

echo "==> Subindo aplicação"
docker compose up -d --build

echo "==> Limpando imagens antigas"
docker image prune -f

echo "==> Status"
docker ps --filter "name=pdf-text-extractor"