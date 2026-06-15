from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

import asyncio
import pyautogui
from config import is_admin, BOT_TOKEN
from aiogram import Bot
from keyboards import get_media_inline

router = Router()

active_media_msg = {
    "chat_id": None,
    "message_id": None,
    "last_track": None
}

async def get_current_track_info():
    try:
        from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
        manager = await MediaManager.request_async()
        session = manager.get_current_session()
        if session:
            info = await session.try_get_media_properties_async()
            title = info.title if info.title else "Неизвестный трек"
            artist = info.artist if info.artist else "Неизвестный автор"
            return title, artist
    except Exception:
        pass
    return None, None

async def track_monitor():
    while True:
        await asyncio.sleep(2)

        if not active_media_msg["message_id"]:
            continue

        title, artist = await get_current_track_info()

        if title != active_media_msg["last_track"]:
            active_media_msg["last_track"] = title

            if title:
                new_text = f"🎧 <b>Сейчас играет:</b>\n👤 Автор: <code>{artist}</code>\n💿 Трек: <code>{title}</code>\n\n🎛️ Управление мультимедиа:"
            else:
                new_text = "🔇 <b>Ничего не играет</b>\nЗапустите музыку на ПК.\n\n🎛️ Управление мультимедиа:"

            try:
                bot = Bot(token=BOT_TOKEN)
                await bot.edit_message_text(
                    chat_id=active_media_msg["chat_id"],
                    message_id=active_media_msg["message_id"],
                    text=new_text,
                    reply_markup=get_media_inline(),
                    parse_mode="HTML"
                )
            except TelegramBadRequest:
                pass
            except Exception as e:
                print(f"Ошибка обновления пульта: {e}")

@router.message(F.text == "🎵 Музыка")
async def show_media_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    title, artist = await get_current_track_info()

    if title:
        text = f"🎧 <b>Сейчас играет:</b>\n👤 Автор: <code>{artist}</code>\n💿 Трек: <code>{title}</code>\n\n🎛️ Управление мультимедиа:"
        active_media_msg["last_track"] = title
    else:
        text = "🔇 <b>Ничего не играет</b>\nЗапустите музыку на ПК.\n\n🎛️ Управление мультимедиа:"
        active_media_msg["last_track"] = None

    msg = await message.answer(text, reply_markup=get_media_inline(), parse_mode="HTML")

    active_media_msg["chat_id"] = msg.chat.id
    active_media_msg["message_id"] = msg.message_id

@router.callback_query(lambda c: c.data.startswith("media_"))
async def handle_media_callbacks(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    action = callback.data.split("_")[1]

    if action == "play":
        pyautogui.press("playpause")
    elif action == "next":
        pyautogui.press("nexttrack")
    elif action == "prev":
        pyautogui.press("prevtrack")
    elif action == "volup":
        pyautogui.press("volumeup")
    elif action == "voldown":
        pyautogui.press("volumedown")
    elif action == "mute":
        pyautogui.press("volumemute")

    await callback.answer("Команда выполнена")
