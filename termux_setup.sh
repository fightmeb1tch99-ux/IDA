#!/data/data/com.termux/files/usr/bin/bash
# IDA — установка на Termux
set -e

echo "=========================================="
echo "  IDA — установка для Termux"
echo "=========================================="

pkg update -y
pkg install -y python git

pip install --upgrade pip
pip install -r requirements-termux.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo ""
  echo ">>> Создан файл .env"
  echo ">>> ОБЯЗАТЕЛЬНО добавь ключ:"
  echo "    GROQ_API_KEY=gsk_..."
  echo ">>> Бесплатно: https://console.groq.com/keys"
  echo ""
fi

mkdir -p memory logs knowledge created_files

echo ""
echo "Готово! Запуск:"
echo "  export GROQ_API_KEY=gsk_твой_ключ"
echo "  python main.py"
echo ""
echo "Или пропиши ключ в .env и:"
echo "  python main.py"
