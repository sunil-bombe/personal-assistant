import os

from tools.task_tools import init_database
from tools.calendar_tools import init_calendar_database
from tools.reminder_tools import init_reminder_database


os.makedirs("database", exist_ok=True)

init_database()
init_calendar_database()
init_reminder_database()

print("Database initialized successfully!")