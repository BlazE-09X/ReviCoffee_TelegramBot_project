from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from database.models import get_connection
from bot.keyboards.items_kb import get_items_keyboard
from bot.keyboards.main_menu import get_main_menu

router = Router()


class AuditStates(StatesGroup):
    choosing_item = State()
    entering_actual = State()


@router.callback_query(F.data == "menu_audit")
async def start_audit(callback: CallbackQuery, state: FSMContext):
    with get_connection() as conn:
        items = conn.execute("SELECT id, name, unit, expected_stock FROM items").fetchall()

    if not items:
        await callback.answer("Сначала добавь товары через меню.", show_alert=True)
        return

    await state.set_state(AuditStates.choosing_item)
    await callback.message.edit_text(
        "Выбери товар для ревизии:",
        reply_markup=get_items_keyboard(items)
    )


@router.callback_query(AuditStates.choosing_item, F.data.startswith("audit_item_"))
async def choose_item(callback: CallbackQuery, state: FSMContext):
    item_id = int(callback.data.replace("audit_item_", ""))

    with get_connection() as conn:
        item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()

    await state.update_data(item_id=item_id, item_name=item["name"], unit=item["unit"], expected=item["expected_stock"])
    await state.set_state(AuditStates.entering_actual)

    await callback.message.edit_text(
        f"Товар: {item['name']}\n"
        f"По учёту сейчас: {item['expected_stock']} {item['unit']}\n\n"
        f"Введи фактический остаток числом:"
    )


@router.message(AuditStates.entering_actual)
async def enter_actual(message: Message, state: FSMContext):
    try:
        actual = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введи число, например: 7.5")
        return

    data = await state.get_data()
    discrepancy = actual - data["expected"]

    with get_connection() as conn:
        conn.execute(
            """INSERT INTO audit_records 
               (item_id, staff_telegram_id, staff_name, actual_stock, expected_stock_at_time, discrepancy)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (data["item_id"], message.from_user.id, message.from_user.full_name,
             actual, data["expected"], discrepancy)
        )
        # обновляем текущий остаток (вариант 1, который мы выбрали)
        conn.execute("UPDATE items SET expected_stock = ? WHERE id = ?", (actual, data["item_id"]))

        items = conn.execute("SELECT id, name, unit, expected_stock FROM items").fetchall()

    sign = "➕" if discrepancy > 0 else ("➖" if discrepancy < 0 else "✅")
    await message.answer(
        f"{sign} {data['item_name']}: расхождение {discrepancy:+.2f} {data['unit']}\n\n"
        f"Выбери следующий товар:",
        reply_markup=get_items_keyboard(items)
    )
    await state.set_state(AuditStates.choosing_item)


@router.callback_query(F.data == "audit_finish")
async def finish_audit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Ревизия завершена ✅", reply_markup=get_main_menu())
