import io
import asyncio
from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile

from config import is_admin

router = Router()

@router.message(F.text == "📸 Скриншот")
async def take_screenshot(message: Message):
    if not is_admin(message.from_user.id):
        return

    try:
        buf = await asyncio.to_thread(_make_screenshot)
        photo = BufferedInputFile(buf.getvalue(), filename="screenshot.jpg")
        await message.answer_photo(photo=photo, caption="📸 Скриншот экрана")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

def _make_screenshot() -> io.BytesIO:
    import mss
    from PIL import Image

    with mss.MSS() as sct:
        monitor = sct.monitors[0]
        img = sct.grab(monitor)
        pic = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

    max_width = 1920
    if pic.width > max_width:
        ratio = max_width / pic.width
        pic = pic.resize((max_width, int(pic.height * ratio)), Image.LANCZOS)

    buf = io.BytesIO()
    pic.save(buf, format="JPEG", quality=75)
    buf.seek(0)
    return buf
