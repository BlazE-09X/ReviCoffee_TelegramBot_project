from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.keyboards.main_menu import get_main_menu
from bot.middlewares.roles import is_manager

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    manager = is_manager(message.from_user.id)
    role_text = "менеджер" if manager else "бариста"
    await message.answer(
        f"Привет! Я бот для ревизии кофейни ☕ (роль: {role_text})\nВыбери действие:",
        reply_markup=get_main_menu(manager)
    )