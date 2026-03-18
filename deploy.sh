#!/usr/bin/env bash
set -e

cd /opt/apps/pdf-text-extractor

echo "==> Atualizando código"
git fetch origin
git checkout main
git pull origin main

echo "==> Subindo aplicação"
docker compose up -d --build

echo "==> Limpando imagens antigas sem uso" 
docker image prune -f

echo "==> Status final"
docker ps --filter "name=pdf-text-extractor"