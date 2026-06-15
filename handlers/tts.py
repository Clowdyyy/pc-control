import asyncio
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from config import is_admin

router = Router()

RUSSIAN_VOICE = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_RU-RU_IRINA_11.0"

@router.message(F.text == "🔊 Озвучить")
async def tts_ask(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("🔊 Отправь текст: <code>/say привет мир</code>", parse_mode="HTML")

@router.message(Command("say"))
async def say_text(message: Message, command: CommandObject):
    if not is_admin(message.from_user.id):
        return
    if not command.args:
        await message.answer("Использование: <code>/say привет мир</code>", parse_mode="HTML")
        return

    await message.answer("🔊 Озвучиваю...")
    try:
        await asyncio.to_thread(_speak, command.args)
        await message.answer("✅ Готово!")
    except ImportError:
        await message.answer("❌ Установи pyttsx3: <code>pip install pyttsx3</code>", parse_mode="HTML")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

def _speak(text: str):
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("voice", RUSSIAN_VOICE)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
