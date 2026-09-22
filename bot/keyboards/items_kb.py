from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_items_keyboard(items: list) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"{item['name']} ({item['unit']})", callback_data=f"audit_item_{item['id']}")]
        for item in items
    ]
    buttons.append([InlineKeyboardButton(text="✅ Завершить ревизию", callback_data="audit_finish")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)