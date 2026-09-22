from aiogram import Router, F
from aiogram.types import CallbackQuery
from analytics.reports import get_discrepancy_summary
from bot.keyboards.main_menu import get_main_menu

router = Router()


@router.callback_query(F.data == "menu_report")
async def show_report(callback: CallbackQuery):
    summary = get_discrepancy_summary(days=30)

    if not summary["items"]:
        await callback.message.edit_text("Пока нет данных ревизий за 30 дней.", reply_markup=get_main_menu())
        return

    text = "📊 Отчёт за 30 дней:\n\n"
    for item in summary["items"]:
        sign = "🔴" if item["total_discrepancy"] < 0 else "🟢"
        text += f"{sign} {item['item_name']}: {item['total_discrepancy']:+.2f} {item['unit']}"
        if item["loss_value"] > 0:
            text += f" (потери ≈ {item['loss_value']:.0f}₸)"
        text += "\n"

    text += f"\n💸 Общие потери: ≈ {summary['total_loss_value']:.0f}₸"

    await callback.message.edit_text(text, reply_markup=get_main_menu())