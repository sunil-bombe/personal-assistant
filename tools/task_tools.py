import sqlite3
from datetime import datetime


DB_NAME = "database/assistant.db"


def init_database():
    """Initialize the tasks database."""

    conn = sqlite3.connect(DB_NAME)
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

    conn.commit()
    conn.close()


def add_task(title: str, due_date: str = None) -> dict:
    """
    Add a new task to the personal task list.

    Args:
        title: Description of the task.
        due_date: Optional due date.

    Returns:
        Status of the task creation.
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, due_date, created_at)
        VALUES (?, ?, ?)
        """,
        (
            title,
            due_date,
            datetime.now().isoformat()
        )
    )

    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return {
        "status": "success",
        "message": f"Task '{title}' added successfully",
        "task_id": task_id
    }


def get_tasks() -> dict:
    """
    Get all pending tasks.

    Returns:
        List of pending tasks.
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, due_date, status
        FROM tasks
        WHERE status = 'pending'
        ORDER BY due_date
    """)

    rows = cursor.fetchall()

    conn.close()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "due_date": row[2],
            "status": row[3]
        })

    return {
        "status": "success",
        "tasks": tasks
    }


def complete_task(task_id: int) -> dict:
    """
    Mark a task as completed.

    Args:
        task_id: ID of the task.

    Returns:
        Status message.
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET status = 'completed'
        WHERE id = ?
        """,
        (task_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return {
            "status": "error",
            "message": "Task not found"
        }

    conn.close()

    return {
        "status": "success",
        "message": f"Task {task_id} marked as completed"
    }