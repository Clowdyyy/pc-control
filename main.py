import sys
import asyncio
import ctypes

import pyautogui
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, ADMIN_ID
from keyboards import get_main_keyboard
from handlers import register_all_handlers
from handlers.media import track_monitor

if sys.platform == "win32":
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)

pyautogui.FAILSAFE = False

if not BOT_TOKEN or not ADMIN_ID:
    exit("Ошибка: Проверьте файл .env — BOT_TOKEN и ADMIN_ID обязательны!")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

register_all_handlers(dp)

async def main():
    print("Помощник готов к работе...")

    if ADMIN_ID:
        try:
            await bot.send_message(
                chat_id=ADMIN_ID,
                text="🟢 <b>Ноутбук включён!</b>\nАссистент запущен и готов к работе.",
                reply_markup=get_main_keyboard(),
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Не удалось отправить уведомление: {e}")

    asyncio.create_task(track_monitor())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
