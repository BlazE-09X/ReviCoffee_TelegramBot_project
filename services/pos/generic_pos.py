import requests
from datetime import datetime
from services.pos.base import POSAdapter


class GenericPOSAdapter(POSAdapter):
    """Шаблон адаптера под произвольную POS-систему.
    При подключении конкретной кассы — копируем этот файл, переименовываем класс
    и подставляем реальные эндпоинты/поля ответа."""

    def __init__(self, api_token: str, base_url: str):
        self.api_token = api_token
        self.base_url = base_url

    def get_sales_for_period(self, date_from: datetime, date_to: datetime) -> list[dict]:
        response = requests.get(
            f"{self.base_url}/sales",
            headers={"Authorization": f"Bearer {self.api_token}"},
            params={"from": date_from.isoformat(), "to": date_to.isoformat()}
        )
        data = response.json()

        return [
            {"drink_name": item["name"], "quantity": item["sold_count"]}
            for item in data.get("sales", [])
        ]