from ai.gemini_client import ask_ai
from analytics.reports import get_discrepancy_summary, get_staff_summary


def explain_discrepancies(days: int = 30) -> str:
    summary = get_discrepancy_summary(days)

    prompt = f"""Ты помощник менеджера кофейни. Вот данные ревизии за {days} дней (JSON):

{summary}

Дай короткий человеческий анализ (3-5 предложений на русском):
- какие позиции проблемные
- есть ли что-то, что стоит проверить
- не обвиняй конкретных людей, только товары/паттерны
Не выдумывай цифры, которых нет в данных."""

    return ask_ai(prompt)


def answer_manager_question(question: str, days: int = 30) -> str:
    summary = get_discrepancy_summary(days)
    staff = get_staff_summary(days)

    prompt = f"""Ты помощник менеджера кофейни. Вот данные за {days} дней:

Расхождения по товарам: {summary}
Сводка по сотрудникам: {staff}

Вопрос менеджера: "{question}"

Ответь на русском, опираясь ТОЛЬКО на эти данные. Если данных недостаточно — так и скажи."""

    return ask_ai(prompt)