import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict


DB_PATH = Path("database") / "assistant.db"


def init_calendar_database() -> None:
    """Create the `meetings` table if it doesn't exist."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                meeting_time TEXT NOT NULL,
                duration INTEGER,
                created_at TEXT
            )
        """)


def add_meeting(title: str, meeting_time: str, duration: int = 30) -> Dict:
    """Schedule a meeting and return status with the new meeting id."""

    created_at = datetime.now().isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO meetings
            (title, meeting_time, duration, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (title, meeting_time, duration, created_at),
        )
        meeting_id = cursor.lastrowid

    return {"status": "success", "message": f"Meeting '{title}' scheduled", "meeting_id": meeting_id}


def get_upcoming_meetings() -> Dict:
    """Return meetings whose meeting_time is greater than or equal to now."""

    now = datetime.now().isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, title, meeting_time, duration
            FROM meetings
            WHERE meeting_time >= ?
            ORDER BY meeting_time
            """,
            (now,),
        )
        rows = cursor.fetchall()

    meetings = [{"id": r[0], "title": r[1], "meeting_time": r[2], "duration": r[3]} for r in rows]

    return {"status": "success", "meetings": meetings}