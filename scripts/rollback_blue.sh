#!/usr/bin/env bash
set -euo pipefail

scripts/switch_traffic.sh blue
scripts/smoke.sh http://127.0.0.1:18080
