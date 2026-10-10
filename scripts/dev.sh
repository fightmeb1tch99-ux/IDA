#!/usr/bin/env bash
# IDA quick dev — delegates to unified launcher
set -e
cd "$(dirname "$0")/.."
exec ./start.sh "${1:-all}"
