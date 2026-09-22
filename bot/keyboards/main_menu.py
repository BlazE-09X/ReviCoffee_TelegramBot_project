from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu(is_manager: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📝 Начать ревизию", callback_data="menu_audit")],
    ]

    if is_manager:
        buttons += [
            [InlineKeyboardButton(text="📦 Список товаров", callback_data="menu_items")],
            [InlineKeyboardButton(text="➕ Добавить товар", callback_data="menu_additem")],
            [InlineKeyboardButton(text="📊 Отчёт", callback_data="menu_report")],
            [InlineKeyboardButton(text="🤖 Спросить ИИ", callback_data="menu_ask_ai")],
        ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)