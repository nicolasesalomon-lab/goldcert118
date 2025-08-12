#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

npm --prefix frontend install
npm --prefix frontend run build
rm -rf backend/app/static/*
cp -r frontend/dist/* backend/app/static/
echo "Build complete"
