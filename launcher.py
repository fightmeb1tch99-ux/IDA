#!/usr/bin/env python3
"""
IDA unified launcher — one command to run the stack.

Usage:
  python launcher.py              # auto: web + cli (bots if tokens)
  python launcher.py all          # same
  python launcher.py cli          # only terminal agent
  python launcher.py web          # only web dashboard :8000
  python launcher.py bots         # telegram + discord if tokens set
  python launcher.py status       # show what would start
"""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

CHILDREN: list[subprocess.Popen] = []


def has_token(name: str) -> bool:
    val = (os.getenv(name) or "").strip()
    return bool(val) and not val.startswith("your_") and "вставь" not in val.lower()


def banner():
    print(
        """
╔════════════════════════════════════════════════════════════════╗
║   ██╗██████╗  █████╗                                           ║
║   ██║██╔══██╗██╔══██╗                                          ║
║   ██║██║  ██║███████║                                          ║
║   ██║██║  ██║██╔══██║                                          ║
║   ██║██████╔╝██║  ██║                                          ║
║   ╚═╝╚═════╝ ╚═╝  ╚═╝                                          ║
║                                                                ║
║     Инновационный Динамический Помощник  •  v5.3               ║
║     one-command launcher                                       ║
╚════════════════════════════════════════════════════════════════╝
"""
    )


def spawn(name: str, cmd: list[str], env: dict | None = None) -> subprocess.Popen | None:
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    log_path = ROOT / "logs" / f"{name}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_f = open(log_path, "a", encoding="utf-8")
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=str(ROOT),
            env=full_env,
            stdout=log_f,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        CHILDREN.append(proc)
        print(f"  ✓ {name}  pid={proc.pid}  log=logs/{name}.log")
        return proc
    except Exception as e:
        print(f"  ✗ {name} failed: {e}")
        log_f.close()
        return None


def stop_children(*_args):
    print("\nОстанавливаю сервисы...")
    for proc in CHILDREN:
        if proc.poll() is None:
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except Exception:
                try:
                    proc.terminate()
                except Exception:
                    pass
    time.sleep(0.5)
    for proc in CHILDREN:
        if proc.poll() is None:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
    print("Готово. До связи.")
    sys.exit(0)


def ensure_env():
    env_path = ROOT / ".env"
    example = ROOT / ".env.example"
    if not env_path.exists() and example.exists():
        env_path.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
        print("Создал .env из .env.example — добавь GROQ_API_KEY")
    if not has_token("GROQ_API_KEY") and not has_token("OPENAI_API_KEY"):
        print("⚠  Нет GROQ_API_KEY / OPENAI_API_KEY — LLM будет ограничен")
        print("   Бесплатно: https://console.groq.com/keys\n")


def start_web() -> subprocess.Popen | None:
    """Единый API: HTTP + WebSocket + профиль + TTS на :8000."""
    return spawn(
        "api",
        [sys.executable, "api_server.py"],
    )


def start_realtime() -> subprocess.Popen | None:
    """Realtime встроен в api_server (:8000/ws). Отдельный процесс не нужен."""
    print("  · realtime  встроен в api_server (/ws)")
    return None


def start_telegram() -> subprocess.Popen | None:
    if not has_token("TELEGRAM_BOT_TOKEN"):
        print("  · telegram  пропуск (нет TELEGRAM_BOT_TOKEN)")
        return None
    return spawn("telegram", [sys.executable, "telegram_bot.py"])


def start_discord() -> subprocess.Popen | None:
    if not has_token("DISCORD_BOT_TOKEN"):
        print("  · discord   пропуск (нет DISCORD_BOT_TOKEN)")
        return None
    return spawn(
        "discord",
        [sys.executable, "-m", "discord_bot.bot"],
    )


def run_cli():
    from main import interactive_mode
    from brain import Brain
    from memory_manager import MemoryManager

    memory_mgr = MemoryManager()
    brain = Brain(memory_mgr.load())
    interactive_mode(brain)


def cmd_status():
    banner()
    print("Что поднимется при `python launcher.py all`:\n")
    print("  api       → Unified API :8000 (chat + /ws + profile + tts)")
    print("  cli       → интерактив в этом терминале")
    print(
        f"  telegram  → {'да' if has_token('TELEGRAM_BOT_TOKEN') else 'нет (токен не задан)'}"
    )
    print(
        f"  discord   → {'да' if has_token('DISCORD_BOT_TOKEN') else 'нет (токен не задан)'}"
    )
    print(
        f"  LLM       → {'Groq' if has_token('GROQ_API_KEY') else 'OpenAI' if has_token('OPENAI_API_KEY') else 'нет ключа'}"
    )
    print()


def cmd_all(with_cli: bool = True):
    banner()
    ensure_env()
    signal.signal(signal.SIGINT, stop_children)
    signal.signal(signal.SIGTERM, stop_children)

    print("Запуск сервисов:\n")
    start_web()
    start_realtime()
    start_telegram()
    start_discord()
    time.sleep(1.2)
    print("\nAPI:      http://127.0.0.1:8000")
    print("WebSocket: ws://127.0.0.1:8000/ws  (аватар + смартфон)")
    print("Профиль:  http://127.0.0.1:8000/api/profile")
    print("Логи: logs/*.log\n")

    if with_cli:
        try:
            run_cli()
        finally:
            stop_children()
    else:
        print("Фоновый режим. Ctrl+C — стоп.")
        while True:
            time.sleep(2)
            dead = [p for p in CHILDREN if p.poll() is not None]
            if dead and len(dead) == len(CHILDREN):
                print("Все процессы завершились.")
                break


def main():
    parser = argparse.ArgumentParser(
        description="IDA — единый запуск всего стека",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python launcher.py           # web + боты + CLI
  python launcher.py web       # только веб-дашборд
  python launcher.py cli       # только терминал
  python launcher.py bots      # только боты
  python launcher.py status    # что запустится
  ./start.sh                   # то же что all
""",
    )
    parser.add_argument(
        "mode",
        nargs="?",
        default="all",
        choices=["all", "cli", "web", "bots", "status"],
        help="режим запуска (default: all)",
    )
    parser.add_argument(
        "--no-cli",
        action="store_true",
        help="не открывать интерактивный CLI (только фоновые сервисы)",
    )
    args = parser.parse_args()

    if args.mode == "status":
        cmd_status()
        return

    if args.mode == "cli":
        banner()
        ensure_env()
        run_cli()
        return

    if args.mode == "web":
        banner()
        ensure_env()
        signal.signal(signal.SIGINT, stop_children)
        signal.signal(signal.SIGTERM, stop_children)
        print("Запуск Unified API:\n")
        start_web()
        print("\nhttp://127.0.0.1:8000  ws://127.0.0.1:8000/ws  — Ctrl+C стоп")
        while True:
            time.sleep(3600)

    if args.mode == "bots":
        banner()
        ensure_env()
        signal.signal(signal.SIGINT, stop_children)
        signal.signal(signal.SIGTERM, stop_children)
        print("Запуск ботов:\n")
        start_telegram()
        start_discord()
        if not CHILDREN:
            print("Нечего запускать — добавь токены в .env")
            return
        print("\nCtrl+C — стоп")
        while True:
            time.sleep(3600)

    # all
    cmd_all(with_cli=not args.no_cli)


if __name__ == "__main__":
    main()
