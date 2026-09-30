import os
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is missing. "
            "Set it in your environment variables."
        )

    return psycopg2.connect(database_url)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id SERIAL PRIMARY KEY,
            query TEXT NOT NULL,
            answer TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()


def save_search(query, answer):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO searches
        (query, answer, created_at)
        VALUES (%s, %s, %s)
        """,
        (
            query,
            answer,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    cursor.close()
    connection.close()


def get_history(limit=20):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, query, created_at
        FROM searches
        ORDER BY id DESC
        LIMIT %s
        """,
        (limit,)
    )

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


def clear_history():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM searches")

    connection.commit()
    cursor.close()
    connection.close()