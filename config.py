import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_PATH = os.getenv("DB_PATH", "coffeeaudit.db")

# ID менеджеров через запятую в .env, например: MANAGER_IDS=123456789,987654321
MANAGER_IDS = [int(x) for x in os.getenv("MANAGER_IDS", "").split(",") if x.strip()]

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY не найден в .env")

if not DB_PATH:
    raise ValueError("DB_PATH не найден в .env")