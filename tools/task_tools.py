import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict


DB_PATH = Path("database") / "assistant.db"


def init_database() -> None:
    """Initialize the tasks database (creates table if missing).

    Creates the `tasks` table with fields: id, title, due_date, status, created_at.
    """

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                due_date TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT
            )
        """)


def add_task(title: str, due_date: Optional[str] = None) -> Dict:
    """Add a new task to the personal task list.

    Args:
        title: Description of the task.
        due_date: Optional due date in ISO format (YYYY-MM-DD or full datetime).

    Returns:
        A dict containing status, message, and new task id.
    """

    created_at = datetime.now().isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tasks (title, due_date, created_at)
            VALUES (?, ?, ?)
            """,
            (title, due_date, created_at),
        )
        task_id = cursor.lastrowid

    return {
        "status": "success",
        "message": f"Task '{title}' added successfully",
        "task_id": task_id,
    }


def get_tasks() -> Dict:
    """Return all pending tasks ordered by due date.

    Returns a dict with status and a list of task objects.
    """

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, title, due_date, status
            FROM tasks
            WHERE status = 'pending'
            ORDER BY due_date IS NULL, due_date
            """
        )
        rows = cursor.fetchall()

    tasks = [
        {"id": r[0], "title": r[1], "due_date": r[2], "status": r[3]}
        for r in rows
    ]

    return {"status": "success", "tasks": tasks}


def complete_task(task_id: int) -> Dict:
    """Mark a task as completed by id.

    Returns an error dict if no row was updated.
    """

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE tasks
            SET status = 'completed'
            WHERE id = ?
            """,
            (task_id,),
        )
        updated = cursor.rowcount

    if updated == 0:
        return {"status": "error", "message": "Task not found"}

    return {"status": "success", "message": f"Task {task_id} marked as completed"}