#!/usr/bin/env bash
set -euo pipefail

docker compose -f docker-compose.blue.yml up -d --build
docker compose -f docker-compose.green.yml up -d --build

scripts/smoke.sh http://127.0.0.1:8001
scripts/smoke.sh http://127.0.0.1:8002

scripts/switch_traffic.sh blue
docker compose -f docker-compose.proxy.yml up -d
scripts/smoke.sh http://127.0.0.1:18080

scripts/switch_traffic.sh green
scripts/smoke.sh http://127.0.0.1:18080

scripts/rollback_blue.sh
