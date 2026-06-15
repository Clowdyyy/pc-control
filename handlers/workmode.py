import os
import subprocess
from aiogram import Router, F
from aiogram.types import Message

from config import is_admin

router = Router()

APPS = {
    "IntelliJ IDEA": r"C:\Program Files\JetBrains\IntelliJ IDEA Community Edition 2024.2.1\bin\idea64.exe",
    "Spotify": os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe"),
    "Firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
}

@router.message(F.text == "💼 Работа")
async def start_work_mode(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer("💼 Запускаю рабочие программы...")

    results = []
    for name, path in APPS.items():
        if os.path.exists(path):
            try:
                subprocess.Popen([path], cwd=os.path.dirname(path))
                results.append(f"✅ {name}")
            except Exception as e:
                results.append(f"❌ {name}: {e}")
        else:
            results.append(f"⚠️ {name}: не найден")

    await message.answer("💼 <b>Результат:</b>\n" + "\n".join(results), parse_mode="HTML")
