import os
import platform
import asyncio
import html
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram.exceptions import TelegramBadRequest
import psutil
import pyautogui
import pyperclip
from dotenv import load_dotenv  

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID")) if os.getenv("ADMIN_ID") else None

if not TOKEN or not ADMIN_ID:
    exit("Ошибка: Проверьте, что файлы .env создан и переменные BOT_TOKEN и ADMIN_ID заполнены!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_main_keyboard():
    kb = [
        [KeyboardButton(text="📊 Статус системы"), KeyboardButton(text="📋 Буфер обмена")],
        [KeyboardButton(text="🎵 Музыкальный пульт"), KeyboardButton(text="⚙️ Тяжелые процессы")],
        [KeyboardButton(text="💤 Режим сна"), KeyboardButton(text="🛑 Выключить ПК")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_media_inline():
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

def is_admin(message: Message) -> bool:
    return message.from_user.id == ADMIN_ID


@dp.message(Command("start"))
async def cmd_start(message: Message):
    if not is_admin(message): return
    await message.answer("🤖 <b>Ассистент ПК запущен.</b> Система готова к удаленному управлению.", reply_markup=get_main_keyboard(), parse_mode="HTML")


@dp.message(lambda message: message.text == "🎵 Музыкальный пульт")
async def show_media_panel(message: Message):
    if not is_admin(message): return
    await message.answer("🎛️ Управление мультимедиа ноутбука:", reply_markup=get_media_inline())

@dp.callback_query(lambda c: c.data.startswith('media_'))
async def handle_media_callbacks(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа", show_alert=True)
        return

    action = callback.data.split('_')[1]
    
    if action == "play": pyautogui.press('playpause')
    elif action == "next": pyautogui.press('nexttrack')
    elif action == "prev": pyautogui.press('prevtrack')
    elif action == "volup": pyautogui.press('volumeup')
    elif action == "voldown": pyautogui.press('volumedown')
    elif action == "mute": pyautogui.press('volumemute')
    
    await callback.answer("Команда выполнена")

@dp.message(lambda message: message.text == "📋 Буфер обмена")
async def get_clipboard(message: Message):
    if not is_admin(message): return
    
    try:
        text = pyperclip.paste()
        if text:
            if len(text) > 3000:
                text = text[:3000] + "\n\n⚠️ <i>[Текст обрезан, так как он слишком длинный для Telegram]</i>"
            
            text = html.escape(text)
            response = f"📋 <b>Текст из буфера ноута:</b>\n\n<code>{text}</code>"
        else:
            response = "Буфер обмена пуст или там не текст."
    except Exception as e:
        response = f"Ошибка чтения буфера: {e}"
        
    try:
        await message.answer(response, parse_mode="HTML")
    except TelegramBadRequest:
        await message.answer("❌ Не удалось отправить буфер обмена из-за ошибки форматирования текста.")

@dp.message(Command("set"))
async def set_clipboard(message: Message, command: CommandObject):
    if not is_admin(message): return
    if not command.args:
        await message.answer("Использование: <code>/set твой текст</code> (он скопируется на ноуте)", parse_mode="HTML")
        return
    
    pyperclip.copy(command.args)
    await message.answer("✅ Текст успешно скопирован в буфер обмена ноутбука! Можно нажимать Ctrl+V.")


@dp.message(lambda message: message.text == "⚙️ Тяжелые процессы")
async def show_processes(message: Message):
    if not is_admin(message): return
    
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    top_proc = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]
    
    msg_text = "<b>🔥 Топ-5 тяжелых процессов в ОЗУ:</b>\n\n"
    for p in top_proc:
        msg_text += f"🔹 <code>{p['name']}</code> (PID: {p['pid']}) — {p['memory_percent']:.1f}%\n"
    
    msg_text += "\n🛑 Чтобы убить зависший процесс, отправь команду:\n<code>/kill PID</code>"
    await message.answer(msg_text, parse_mode="HTML")

@dp.message(Command("kill"))
async def kill_process(message: Message, command: CommandObject):
    if not is_admin(message): return
    if not command.args:
        await message.answer("Укажи PID процесса. Пример: <code>/kill 1234</code>", parse_mode="HTML")
        return
        
    try:
        pid = int(command.args)
        target_proc = psutil.Process(pid)
        p_name = target_proc.name()
        
        killed_count = 0
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] == p_name:
                    proc.kill()
                    killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        response = f"💥 <b>Программа полностью закрыта!</b>\nУничтожено процессов <code>{p_name}</code>: {killed_count} шт."
        
    except psutil.NoSuchProcess:
        response = "❌ Процесс с таким PID уже не существует."
    except psutil.AccessDenied:
        response = "🔒 Недостаточно прав. Попробуй запустить терминал от имени Администратора."
    except ValueError:
        response = "PID должен быть числом."
        
    await message.answer(response, parse_mode="HTML")


@dp.message(lambda message: message.text == "📊 Статус системы")
async def system_status(message: Message):
    if not is_admin(message): return
    
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()
    
    status_text = f"🖥️ <b>Статус ноутбука:</b>\n\n🔥 Загрузка ЦП: {cpu}%\n🧠 Загрузка ОЗУ: {ram}%\n"
    if battery:
        plugged = "Заряжается" if battery.power_plugged else "От батареи"
        status_text += f"🔋 Батарея: {battery.percent}% ({plugged})\n"
        
    await message.answer(status_text, parse_mode="HTML")

@dp.message(lambda message: message.text == "💤 Режим сна")
async def go_to_sleep(message: Message):
    if not is_admin(message): return
    await message.answer("Отправляю в сон...")
    if platform.system() == "Windows":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

@dp.message(lambda message: message.text == "🛑 Выключить ПК")
async def shutdown_pc(message: Message):
    if not is_admin(message): return
    await message.answer("Выключаю...")
    if platform.system() == "Windows":
        os.system("shutdown /s /t 5")

async def main():
    print("Помощник готов к работе...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())