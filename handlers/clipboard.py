import html as html_module
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

import pyperclip
from config import is_admin

router = Router()

@router.message(F.text == "📋 Буфер")
async def get_clipboard(message: Message):
    if not is_admin(message.from_user.id):
        return

    try:
        text = pyperclip.paste()
        if text:
            if len(text) > 3000:
                text = text[:3000] + "\n\n⚠️ <i>[Текст обрезан]</i>"
            text = html_module.escape(text)
            response = f"📋 <b>Текст из буфера обмена:</b>\n\n<code>{text}</code>"
        else:
            response = "Буфер обмена пуст или там не текст."
    except Exception as e:
        response = f"Ошибка чтения буфера: {e}"

    try:
        await message.answer(response, parse_mode="HTML")
    except Exception:
        await message.answer("❌ Не удалось отправить буфер из-за ошибки форматирования.")

@router.message(Command("set"))
async def set_clipboard(message: Message, command: CommandObject):
    if not is_admin(message.from_user.id):
        return
    if not command.args:
        await message.answer("Использование: <code>/set текст</code>", parse_mode="HTML")
        return

    pyperclip.copy(command.args)
    await message.answer("✅ Текст скопирован в буфер обмена!")
