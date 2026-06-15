import os
import platform
import ctypes
from aiogram import Router, F
from aiogram.types import Message

from config import is_admin

router = Router()

@router.message(F.text == "💤 Сон")
async def go_to_sleep(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("Отправляю в сон...")
    if platform.system() == "Windows":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

@router.message(F.text == "🛑 Выключить")
async def shutdown_pc(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("Выключаю...")
    if platform.system() == "Windows":
        os.system("shutdown /s /t 5")

@router.message(F.text == "🔒 Заблокировать")
async def lock_screen(message: Message):
    if not is_admin(message.from_user.id):
        return
    try:
        ctypes.windll.user32.LockWorkStation()
        await message.answer("🔒 Экран заблокирован!")
    except Exception as e:
        await message.answer(f"❌ Ошибка блокировки: {e}")
