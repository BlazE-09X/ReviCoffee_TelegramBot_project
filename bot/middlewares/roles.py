from config import MANAGER_IDS


def is_manager(telegram_id: int) -> bool:
    return telegram_id in MANAGER_IDS