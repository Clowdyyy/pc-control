from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

import psutil
from config import is_admin

router = Router()

@router.message(F.text == "⚙️ Процессы")
async def show_processes(message: Message):
    if not is_admin(message.from_user.id):
        return

    processes = []
    for proc in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    top_proc = sorted(processes, key=lambda x: x["memory_percent"], reverse=True)[:5]

    msg_text = "<b>🔥 Топ-5 тяжёлых процессов в ОЗУ:</b>\n\n"
    for p in top_proc:
        msg_text += f"🔹 <code>{p['name']}</code> (PID: {p['pid']}) — {p['memory_percent']:.1f}%\n"

    msg_text += "\n🛑 Чтобы убить процесс: <code>/kill PID</code>"
    await message.answer(msg_text, parse_mode="HTML")

@router.message(Command("kill"))
async def kill_process(message: Message, command: CommandObject):
    if not is_admin(message.from_user.id):
        return
    if not command.args:
        await message.answer("Укажи PID: <code>/kill 1234</code>", parse_mode="HTML")
        return

    try:
        pid = int(command.args)
        target_proc = psutil.Process(pid)
        p_name = target_proc.name()

        killed_count = 0
        for proc in psutil.process_iter(["name"]):
            try:
                if proc.info["name"] == p_name:
                    proc.kill()
                    killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        response = f"💥 <b>Программа закрыта!</b>\nУничтожено процессов <code>{p_name}</code>: {killed_count} шт."

    except psutil.NoSuchProcess:
        response = "❌ Процесс с таким PID уже не существует."
    except psutil.AccessDenied:
        response = "🔒 Недостаточно прав. Запусти от имени Администратора."
    except ValueError:
        response = "PID должен быть числом."

    await message.answer(response, parse_mode="HTML")
