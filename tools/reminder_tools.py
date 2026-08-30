import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict


DB_PATH = Path("database") / "assistant.db"


def init_reminder_database() -> None:
    """Create the `reminders` table if it doesn't exist."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                reminder_time TEXT NOT NULL,
                notified INTEGER DEFAULT 0
            )
        """)


def create_reminder(message: str, reminder_time: str) -> Dict:
    """Insert a reminder into the DB.

    `reminder_time` should be an ISO timestamp or date string.
    Returns a dict with the new reminder id.
    """

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO reminders
            (message, reminder_time)
            VALUES (?, ?)
            """,
            (message, reminder_time),
        )
        reminder_id = cursor.lastrowid

    return {"status": "success", "message": f"Reminder created: {message}", "reminder_id": reminder_id}


def get_reminders() -> Dict:
    """Return pending (not yet notified) reminders ordered by reminder_time."""

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, message, reminder_time
            FROM reminders
            WHERE notified = 0
            ORDER BY reminder_time
            """
        )
        rows = cursor.fetchall()

    reminders = [{"id": r[0], "message": r[1], "reminder_time": r[2]} for r in rows]

    return {"status": "success", "reminders": reminders}