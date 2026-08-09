#!/data/data/com.termux/files/usr/bin/bash
# IDA — установка на Termux (без поломки pip)
set -e

echo "=========================================="
echo "  IDA — установка для Termux"
echo "=========================================="

pkg update -y
pkg install -y python git

# На Termux НЕЛЬЗЯ делать: pip install --upgrade pip
# Ставим пакеты напрямую
pip install python-dotenv requests colorama groq

if [ ! -f .env ]; then
  cp .env.example .env 2>/dev/null || cat > .env << 'ENV'
# Получи бесплатный ключ: https://console.groq.com/keys
GROQ_API_KEY=
ENV
  echo ""
  echo ">>> Создан файл .env"
fi

mkdir -p memory logs knowledge created_files

echo ""
echo "=========================================="
echo "  ДАЛЬШЕ СДЕЛАЙ ТАК:"
echo "=========================================="
echo "1) Открой .env:"
echo "     nano .env"
echo ""
echo "2) Впиши ключ Groq (бесплатно):"
echo "     GROQ_API_KEY=gsk_............"
echo ""
echo "   Ключ взять здесь:"
echo "   https://console.groq.com/keys"
echo ""
echo "3) Сохрани (Ctrl+O, Enter, Ctrl+X) и запусти:"
echo "     python main.py"
echo ""
echo "ВАЖНО: не используй старый/битый OPENAI ключ."
echo "Для Termux достаточно только GROQ_API_KEY."
echo "=========================================="
