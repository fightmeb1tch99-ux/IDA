"""
Manages the Mineflayer (Node.js) bot process and communicates with it.
IDA can join a Java Edition server and act as a real friend.
"""

import asyncio
import json
import subprocess
import os
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from logger import log_info, log_error, log_warning

from .lore import LoreManager

BOT_SCRIPT = Path(__file__).parent / "bot.js"


class MinecraftBotManager:
    def __init__(self, brain=None):
        self.brain = brain
        self.lore = LoreManager()
        self.process: Optional[subprocess.Popen] = None
        self.connected = False
        self.host: Optional[str] = None
        self.port: int = 25565
        self.username: str = "IDA"
        self._chat_callback: Optional[Callable] = None

    def set_chat_callback(self, cb: Callable):
        """Set function that will receive chat messages from the game."""
        self._chat_callback = cb

    async def connect(self, host: str, port: int = 25565, username: str = "IDA", version: str = "1.20.1") -> Dict[str, Any]:
        """
        Start the Mineflayer bot and connect to a Java Edition server.
        """
        if self.process and self.process.poll() is None:
            return {"ok": False, "error": "Bot already running. Disconnect first."}

        self.host = host
        self.port = port
        self.username = username

        if not BOT_SCRIPT.exists():
            return {"ok": False, "error": f"bot.js not found at {BOT_SCRIPT}"}

        env = os.environ.copy()
        env["MC_HOST"] = host
        env["MC_PORT"] = str(port)
        env["MC_USERNAME"] = username
        env["MC_VERSION"] = version

        try:
            self.process = subprocess.Popen(
                ["node", str(BOT_SCRIPT)],
                cwd=str(BOT_SCRIPT.parent),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            self.connected = True
            log_info(f"Minecraft bot starting → {host}:{port} as {username}")

            # Start reading stdout in background
            asyncio.create_task(self._read_output())

            return {
                "ok": True,
                "message": f"IDA подключается к {host}:{port} как {username}",
                "lore": self.lore.get_prompt_context()
            }
        except FileNotFoundError:
            return {"ok": False, "error": "Node.js не найден. Установи Node.js и mineflayer."}
        except Exception as e:
            log_error("Failed to start Minecraft bot", e)
            return {"ok": False, "error": str(e)}

    async def disconnect(self) -> Dict[str, Any]:
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None
            self.connected = False
            log_info("Minecraft bot disconnected")
            return {"ok": True, "message": "IDA вышла из игры"}
        return {"ok": False, "error": "Бот не был запущен"}

    async def chat(self, message: str) -> Dict[str, Any]:
        """Send a chat message into the game."""
        if not self.connected or not self.process:
            return {"ok": False, "error": "Бот не подключён"}
        # Simple protocol: write to stdin of the node process
        try:
            if self.process.stdin:
                self.process.stdin.write(json.dumps({"type": "chat", "text": message}) + "\n")
                self.process.stdin.flush()
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    async def follow_player(self, player_name: str) -> Dict[str, Any]:
        return await self._send_command({"type": "follow", "player": player_name})

    async def stop_follow(self) -> Dict[str, Any]:
        return await self._send_command({"type": "stop"})

    async def _send_command(self, cmd: Dict[str, Any]) -> Dict[str, Any]:
        if not self.connected or not self.process or not self.process.stdin:
            return {"ok": False, "error": "Бот не подключён"}
        try:
            self.process.stdin.write(json.dumps(cmd) + "\n")
            self.process.stdin.flush()
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    async def _read_output(self):
        """Read lines from the bot process and handle events."""
        if not self.process or not self.process.stdout:
            return
        loop = asyncio.get_event_loop()
        while self.process and self.process.poll() is None:
            try:
                line = await loop.run_in_executor(None, self.process.stdout.readline)
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    await self._handle_event(data)
                except json.JSONDecodeError:
                    log_info(f"[MC Bot] {line}")
            except Exception as e:
                log_error("Error reading bot output", e)
                break
        self.connected = False

    async def _handle_event(self, data: Dict[str, Any]):
        event = data.get("event")
        if event == "chat" and self._chat_callback:
            username = data.get("username", "")
            message = data.get("message", "")
            if username != self.username:
                await self._chat_callback(username, message)
        elif event == "spawn":
            log_info("IDA spawned in the world")
        elif event == "error":
            log_error(f"Bot error: {data.get('message')}")
        elif event == "end":
            log_warning("Bot disconnected from server")
            self.connected = False

    def get_status(self) -> Dict[str, Any]:
        return {
            "connected": self.connected,
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "lore": self.lore.get()
        }
