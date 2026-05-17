#!/usr/bin/env bash
set -euo pipefail

target="${1:-}"
if [[ "${target}" != "blue" && "${target}" != "green" ]]; then
  echo "usage: scripts/switch_traffic.sh blue|green" >&2
  exit 2
fi

cat "nginx/${target}.conf" > nginx/default.conf

if docker ps --format '{{.Names}}' | grep -q '^ml-ops-hw7-proxy$'; then
  docker compose -f docker-compose.proxy.yml exec nginx nginx -s reload
  sleep 1
fi

echo "traffic switched to ${target}"
