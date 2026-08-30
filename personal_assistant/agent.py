from google.adk.agents import Agent

from tools.task_tools import (
    add_task,
    get_tasks,
    complete_task
)

from tools.calendar_tools import (
    add_meeting,
    get_upcoming_meetings
)

from tools.reminder_tools import (
    create_reminder,
    get_reminders
)


def get_current_time() -> dict:
    """
    Returns the current local date and time.
    """

    from datetime import datetime

    now = datetime.now()

    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A")
    }


root_agent = Agent(
    name="personal_assistant",

    model="gemini-2.5-flash",

    description="""
    A personal AI assistant that helps manage
    tasks, meetings, reminders and daily activities.
    """,

    instruction="""
    You are a smart personal laptop assistant.

    Your responsibilities include:

    1. Managing daily tasks
    2. Creating reminders
    3. Scheduling meetings
    4. Showing upcoming meetings
    5. Helping organize daily work

    Always use available tools when the user asks
    to create, retrieve, update or manage tasks,
    meetings or reminders.

    Be concise and helpful.

    When creating dates and times, use ISO format:

    YYYY-MM-DD HH:MM:SS

    Example:

    2026-08-31 10:00:00
    """,

    tools=[
        get_current_time,

        add_task,
        get_tasks,
        complete_task,

        add_meeting,
        get_upcoming_meetings,

        create_reminder,
        get_reminders
    ]
)