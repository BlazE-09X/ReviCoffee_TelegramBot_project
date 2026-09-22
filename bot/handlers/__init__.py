from aiogram import Dispatcher
from bot.handlers.start import router as start_router
from bot.handlers.items import router as items_router
from bot.handlers.audit import router as audit_router
from bot.handlers.recipes import router as recipes_router
from bot.handlers.reports import router as reports_router
from bot.handlers.ai_chat import router as ai_router


def register_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(items_router)
    dp.include_router(audit_router)
    dp.include_router(recipes_router)
    dp.include_router(reports_router)
    dp.include_router(ai_router)