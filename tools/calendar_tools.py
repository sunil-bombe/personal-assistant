import sqlite3
from datetime import datetime


DB_NAME = "database/assistant.db"


def init_calendar_database():

    conn = sqlite3.connect(DB_NAME)
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

    conn.commit()
    conn.close()


def add_meeting(
    title: str,
    meeting_time: str,
    duration: int = 30
) -> dict:
    """
    Schedule a meeting.

    Args:
        title: Meeting title.
        meeting_time: Meeting date and time.
        duration: Meeting duration in minutes.

    Returns:
        Meeting creation status.
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO meetings
        (title, meeting_time, duration, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            title,
            meeting_time,
            duration,
            datetime.now().isoformat()
        )
    )

    conn.commit()

    meeting_id = cursor.lastrowid

    conn.close()

    return {
        "status": "success",
        "message": f"Meeting '{title}' scheduled",
        "meeting_id": meeting_id
    }


def get_upcoming_meetings() -> dict:
    """
    Get all upcoming meetings.

    Returns:
        List of scheduled meetings.
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        SELECT id, title, meeting_time, duration
        FROM meetings
        WHERE meeting_time >= ?
        ORDER BY meeting_time
        """,
        (now,)
    )

    rows = cursor.fetchall()

    conn.close()

    meetings = []

    for row in rows:
        meetings.append({
            "id": row[0],
            "title": row[1],
            "meeting_time": row[2],
            "duration": row[3]
        })

    return {
        "status": "success",
        "meetings": meetings
    }