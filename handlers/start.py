from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config import is_admin
from keyboards import get_main_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer(
        "🤖 <b>Ассистент ПК запущен.</b>\nСистема готова к удалённому управлению.",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )
