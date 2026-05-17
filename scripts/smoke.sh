#!/usr/bin/env bash
set -euo pipefail

base_url="${1:-http://127.0.0.1:8000}"

echo "health:"
curl -fsS --retry 10 --retry-delay 2 --retry-all-errors "${base_url}/health"
echo

echo "predict:"
curl -fsS --retry 10 --retry-delay 2 --retry-all-errors -X POST "${base_url}/predict" \
  -H "Content-Type: application/json" \
  -d '{"x":[1,2,3]}'
echo
