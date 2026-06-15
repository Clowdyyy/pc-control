from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="📊 Статус"), KeyboardButton(text="💻 Инфо"), KeyboardButton(text="💼 Работа")],
        [KeyboardButton(text="📋 Буфер"), KeyboardButton(text="📸 Скриншот"), KeyboardButton(text="📷 Веб-камера")],
        [KeyboardButton(text="🎵 Музыка"), KeyboardButton(text="⚙️ Процессы"), KeyboardButton(text="🔊 Озвучить")],
        [KeyboardButton(text="🔒 Заблокировать"), KeyboardButton(text="💤 Сон"), KeyboardButton(text="🛑 Выключить")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_media_inline() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⏮️ Назад", callback_data="media_prev"),
            InlineKeyboardButton(text="⏯️ Пауза/Старт", callback_data="media_play"),
            InlineKeyboardButton(text="⏭️ Вперед", callback_data="media_next")
        ],
        [
            InlineKeyboardButton(text="🔉 Тише", callback_data="media_voldown"),
            InlineKeyboardButton(text="🔇 Мут", callback_data="media_mute"),
            InlineKeyboardButton(text="🔊 Громче", callback_data="media_volup")
        ]
    ])
    return keyboard
