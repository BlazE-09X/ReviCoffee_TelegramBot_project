from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.models import get_connection
from bot.middlewares.roles import is_manager

router = Router()


@router.message(Command("additem"))
async def cmd_add_item(message: Message):
    if not is_manager(message.from_user.id):
        await message.answer("Эта команда доступна только менеджеру.")
        return

    args = message.text.replace("/additem", "").strip()
    if not args:
        await message.answer(
            "Формат: /additem Название;единица;текущий_остаток;цена_за_единицу\n"
            "Пример: /additem Молоко;л;10;500"
        )
        return

    try:
        name, unit, expected_stock, price = args.split(";")
        expected_stock = float(expected_stock.strip())
        price = float(price.strip())
    except ValueError:
        await message.answer("Неверный формат. Пример: /additem Молоко;л;10;500")
        return

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO items (name, unit, expected_stock, price_per_unit) VALUES (?, ?, ?, ?)",
            (name.strip(), unit.strip(), expected_stock, price)
        )

    await message.answer(f"Добавлено: {name.strip()} — {expected_stock} {unit.strip()}")


@router.message(Command("items"))
async def cmd_list_items(message: Message):
    if not is_manager(message.from_user.id):
        await message.answer("Эта команда доступна только менеджеру.")
        return

    with get_connection() as conn:
        rows = conn.execute("SELECT id, name, unit, expected_stock, price_per_unit FROM items").fetchall()

    if not rows:
        await message.answer("Товаров пока нет. Добавь через /additem")
        return

    text = "📦 Товары:\n\n"
    for row in rows:
        text += f"#{row['id']} • {row['name']}: {row['expected_stock']} {row['unit']} (цена: {row['price_per_unit']}₸)\n"

    await message.answer(text)


@router.message(Command("deleteitem"))
async def cmd_delete_item(message: Message):
    if not is_manager(message.from_user.id):
        await message.answer("Эта команда доступна только менеджеру.")
        return

    args = message.text.replace("/deleteitem", "").strip()
    if not args.isdigit():
        await message.answer("Формат: /deleteitem ID\nID смотри в /items")
        return

    item_id = int(args)
    with get_connection() as conn:
        item = conn.execute("SELECT name FROM items WHERE id = ?", (item_id,)).fetchone()
        if not item:
            await message.answer("Товар с таким ID не найден.")
            return
        conn.execute("DELETE FROM items WHERE id = ?", (item_id,))

    await message.answer(f"Удалено: {item['name']}")


@router.message(Command("edititem"))
async def cmd_edit_item(message: Message):
    if not is_manager(message.from_user.id):
        await message.answer("Эта команда доступна только менеджеру.")
        return

    # Формат: /edititem ID;поле;новое_значение
    # Пример: /edititem 3;price_per_unit;550
    args = message.text.replace("/edititem", "").strip()

    try:
        item_id, field, value = args.split(";")
        item_id = int(item_id.strip())
        field = field.strip()
    except ValueError:
        await message.answer(
            "Формат: /edititem ID;поле;значение\n"
            "Доступные поля: name, unit, expected_stock, price_per_unit\n"
            "Пример: /edititem 3;price_per_unit;550"
        )
        return

    allowed_fields = {"name", "unit", "expected_stock", "price_per_unit"}
    if field not in allowed_fields:
        await message.answer(f"Поле должно быть одним из: {', '.join(allowed_fields)}")
        return

    if field in ("expected_stock", "price_per_unit"):
        try:
            value = float(value.strip())
        except ValueError:
            await message.answer("Для этого поля нужно число.")
            return
    else:
        value = value.strip()

    with get_connection() as conn:
        item = conn.execute("SELECT id FROM items WHERE id = ?", (item_id,)).fetchone()
        if not item:
            await message.answer("Товар с таким ID не найден.")
            return
        conn.execute(f"UPDATE items SET {field} = ? WHERE id = ?", (value, item_id))

    await message.answer(f"Обновлено: товар #{item_id}, {field} = {value}")