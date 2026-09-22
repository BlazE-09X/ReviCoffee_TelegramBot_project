import requests
from datetime import datetime
from services.pos.base import POSAdapter


class PosterAdapter(POSAdapter):
    def __init__(self, api_token: str, account_name: str):
        self.api_token = api_token
        self.base_url = f"https://{account_name}.joinposter.com/api"

    def get_sales_for_period(self, date_from: datetime, date_to: datetime) -> list[dict]:
        # Точный эндпоинт/параметры уточним по реальной документации,
        # когда будет доступ к аккаунту кофейни. Структура ответа ниже — заглушка.
        response = requests.get(
            f"{self.base_url}/dash.getProductsSales",
            params={
                "token": self.api_token,
                "dateFrom": date_from.strftime("%Y-%m-%d"),
                "dateTo": date_to.strftime("%Y-%m-%d"),
            }
        )
        data = response.json()

        # Приводим ответ Poster к нашему общему формату
        return [
            {"drink_name": item["product_name"], "quantity": item["count"]}
            for item in data.get("response", [])
        ]