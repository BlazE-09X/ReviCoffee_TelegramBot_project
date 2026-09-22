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
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                unit TEXT NOT NULL,               -- кг, л, шт
                expected_stock REAL NOT NULL DEFAULT 0,
                price_per_unit REAL NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                staff_telegram_id INTEGER NOT NULL,
                staff_name TEXT,
                actual_stock REAL NOT NULL,
                expected_stock_at_time REAL NOT NULL,
                discrepancy REAL NOT NULL,         -- actual - expected
                data_source TEXT DEFAULT 'manual',  -- manual / pos / scale / photo — задел на будущее
                audit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES items (id)
            )
        """)