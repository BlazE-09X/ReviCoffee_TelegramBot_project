
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.models import get_connection

router = Router()


@router.message(Command("addrecipe"))
async def cmd_add_recipe(message: Message):
    # Формат: /addrecipe Капучино;Молоко;0.2
    # drink;item_name;amount_per_drink
    args = message.text.replace("/addrecipe", "").strip()

    if not args:
        await message.answer(
            "Формат: /addrecipe Напиток;Товар;количество_на_1_напиток\n"
            "Пример: /addrecipe Капучино;Молоко;0.2"
        )
        return

    try:
        drink_name, item_name, amount = args.split(";")
        amount = float(amount.strip())
    except ValueError:
        await message.answer("Неверный формат. Пример: /addrecipe Капучино;Молоко;0.2")
        return

    with get_connection() as conn:
        item = conn.execute("SELECT id FROM items WHERE name = ?", (item_name.strip(),)).fetchone()
        if not item:
            await message.answer(f"Товар «{item_name.strip()}» не найден. Сначала добавь его через /additem")
            return

        drink = conn.execute("SELECT id FROM drinks WHERE name = ?", (drink_name.strip(),)).fetchone()
        if not drink:
            cursor = conn.execute("INSERT INTO drinks (name) VALUES (?)", (drink_name.strip(),))
            drink_id = cursor.lastrowid
        else:
            drink_id = drink["id"]

        conn.execute(
            "INSERT INTO recipe_ingredients (drink_id, item_id, amount_per_drink) VALUES (?, ?, ?)",
            (drink_id, item["id"], amount)
        )

    await message.answer(f"Рецепт добавлен: {drink_name.strip()} → {amount} {item_name.strip()}")

@router.message(Command("recipe"))
async def cmd_show_recipe(message: Message):
    drink_name = message.text.replace("/recipe", "").strip()

    if not drink_name:
        await message.answer("Формат: /recipe Капучино")
        return

    with get_connection() as conn:
        drink = conn.execute("SELECT id FROM drinks WHERE name = ?", (drink_name,)).fetchone()
        if not drink:
            await message.answer(f"Напиток «{drink_name}» не найден.")
            return

        ingredients = conn.execute("""
            SELECT i.name, ri.amount_per_drink, i.unit
            FROM recipe_ingredients ri
            JOIN items i ON i.id = ri.item_id
            WHERE ri.drink_id = ?
        """, (drink["id"],)).fetchall()

    if not ingredients:
        await message.answer(f"У «{drink_name}» пока нет ингредиентов в рецепте.")
        return

    text = f"☕ {drink_name}:\n\n"
    for ing in ingredients:
        text += f"• {ing['name']}: {ing['amount_per_drink']} {ing['unit']}\n"

    await message.answer(text)