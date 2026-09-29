import sqlite3
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "search_history.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            answer TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_search(query, answer):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO searches
        (query, answer, created_at)
        VALUES (?, ?, ?)
        """,
        (
            query,
            answer,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()


def get_history(limit=20):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, query, created_at
        FROM searches
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    results = cursor.fetchall()

    connection.close()

    return results


def clear_history():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("DELETE FROM searches")

    connection.commit()
    connection.close()