#!/usr/bin/env bash
set -e

cd /opt/apps/pdf-text-extractor

git fetch origin
git checkout main
git pull origin main

docker compose up -d --build
docker image prune -f