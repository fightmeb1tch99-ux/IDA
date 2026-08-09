#!/usr/bin/env bash
# IDA quick dev launcher
set -e
cd "$(dirname "$0")/.."

echo "=== IDA Dev ==="
echo "1) Python agent:  python main.py"
echo "2) Realtime:      python -m realtime.bridge"
echo "3) Web:           pnpm dev"
echo ""
echo "Starting realtime bridge on :8765 ..."
python -m realtime.bridge
