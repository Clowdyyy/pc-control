from aiogram import Router

from .start import router as start_router
from .system import router as system_router
from .clipboard import router as clipboard_router
from .media import router as media_router
from .processes import router as processes_router
from .power import router as power_router
from .screenshot import router as screenshot_router
from .tts import router as tts_router
from .webcam import router as webcam_router
from .workmode import router as workmode_router

def register_all_handlers(main_router: Router):
    main_router.include_router(start_router)
    main_router.include_router(system_router)
    main_router.include_router(clipboard_router)
    main_router.include_router(media_router)
    main_router.include_router(processes_router)
    main_router.include_router(power_router)
    main_router.include_router(screenshot_router)
    main_router.include_router(tts_router)
    main_router.include_router(webcam_router)
    main_router.include_router(workmode_router)
