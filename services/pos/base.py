from abc import ABC, abstractmethod
from datetime import datetime


class POSAdapter(ABC):
    """Общий интерфейс для любой кассовой системы.
    Чтобы подключить новую POS — просто наследуемся и реализуем этот метод."""

    @abstractmethod
    def get_sales_for_period(self, date_from: datetime, date_to: datetime) -> list[dict]:
        """
        Должен вернуть список вида:
        [{'drink_name': 'Капучино', 'quantity': 40}, {'drink_name': 'Латте', 'quantity': 20}]
        """
        pass