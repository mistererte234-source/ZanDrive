#!/bin/bash
set -e

echo "=== ZanDrive Deploy ==="

# Pull latest
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build

echo "=== Done ==="
echo "API: http://$(curl -s ifconfig.me):8000"
echo "Docs: http://$(curl -s ifconfig.me):8000/docs"
