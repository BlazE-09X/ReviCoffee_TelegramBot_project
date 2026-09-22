import sqlite3
from contextlib import contextmanager
from config import DB_PATH


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS drinks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipe_ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                drink_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                amount_per_drink REAL NOT NULL,   -- сколько единицы item уходит на 1 напиток
                FOREIGN KEY (drink_id) REFERENCES drinks (id),
                FOREIGN KEY (item_id) REFERENCES items (id)
            )
        """)