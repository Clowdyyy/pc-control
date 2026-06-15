import io
import asyncio
from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile

from config import is_admin

router = Router()

@router.message(F.text == "📷 Веб-камера")
async def take_webcam(message: Message):
    if not is_admin(message.from_user.id):
        return

    try:
        buf = await asyncio.to_thread(_capture_webcam)
        if buf is None:
            await message.answer("❌ Веб-камера не найдена или не отвечает")
            return
        photo = BufferedInputFile(buf.getvalue(), filename="webcam.jpg")
        await message.answer_photo(photo=photo, caption="📷 Фото с веб-камеры")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

def _capture_webcam() -> io.BytesIO | None:
    import cv2
    from PIL import Image

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        return None

    pic = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    buf = io.BytesIO()
    pic.save(buf, format="JPEG", quality=85)
    buf.seek(0)
    return buf
