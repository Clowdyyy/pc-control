from aiogram import Router, F
from aiogram.types import Message

import psutil
from config import is_admin
from utils.system_info import (
    get_cpu_info, get_ram_info, get_gpu_info,
    get_disk_info, get_windows_info
)

router = Router()

@router.message(F.text == "📊 Статус")
async def system_status(message: Message):
    if not is_admin(message.from_user.id):
        return

    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()

    status_text = f"🖥️ <b>Статус ноутбука:</b>\n\n🔥 Загрузка ЦП: {cpu}%\n🧠 Загрузка ОЗУ: {ram}%\n"
    if battery:
        plugged = "Заряжается" if battery.power_plugged else "От батареи"
        status_text += f"🔋 Батарея: {battery.percent}% ({plugged})\n"

    await message.answer(status_text, parse_mode="HTML")

@router.message(F.text == "💻 Инфо")
async def system_info(message: Message):
    if not is_admin(message.from_user.id):
        return

    cpu = get_cpu_info()
    ram = get_ram_info()
    gpu = get_gpu_info()
    win = get_windows_info()
    disks = get_disk_info()

    text = "💻 <b>Подробная информация о системе:</b>\n\n"

    text += "🔸 <b>Процессор:</b>\n"
    text += f"  Модель: <code>{cpu['model']}</code>\n"
    text += f"  Ядра: {cpu['cores_physical']} физ. / {cpu['cores_logical']} лог.\n"
    text += f"  Частота: {cpu['freq_current']} (макс. {cpu['freq_max']})\n\n"

    text += "🔸 <b>Оперативная память:</b>\n"
    text += f"  Всего: {ram['total']}\n"
    text += f"  Используется: {ram['used']} ({ram['percent']})\n"
    text += f"  Свободно: {ram['available']}\n\n"

    text += "🔸 <b>Видеокарта:</b>\n"
    text += f"  Модель: <code>{gpu['name']}</code>\n"
    text += f"  VRAM: {gpu['vram']}\n\n"

    text += "🔸 <b>Windows:</b>\n"
    text += f"  Версия: {win['system']} {win['release']}\n"
    text += f"  Сборка: {win['version']}\n"
    text += f"  Архитектура: {win['machine']}\n\n"

    if disks:
        text += "🔸 <b>Диски:</b>\n"
        for d in disks:
            text += f"  {d['device']} ({d['mountpoint']}): {d['used']} / {d['total']} ({d['percent']})\n"

    await message.answer(text, parse_mode="HTML")
