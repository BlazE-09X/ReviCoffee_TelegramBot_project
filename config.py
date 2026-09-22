import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_PATH = os.getenv("DB_PATH", "coffeeaudit.db")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY не найден в .env")

if not DB_PATH:
    raise ValueError("DB_PATH не найден в .env")