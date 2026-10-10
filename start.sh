#!/usr/bin/env bash
# IDA — one command start
set -e
cd "$(dirname "$0")"

if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
  echo "Создал .env — добавь GROQ_API_KEY (бесплатно: https://console.groq.com/keys)"
fi

MODE="${1:-all}"
exec python3 launcher.py "$MODE" "${@:2}"
