from datetime import datetime
from collections.abc import Callable
from typing import Any

from google.adk.agents import Agent

from personal_assistant.model_config import get_model
from tools.calendar_tools import add_meeting, get_upcoming_meetings
from tools.reminder_tools import create_reminder, get_reminders
from tools.task_tools import add_task, complete_task, get_tasks


def get_current_time() -> dict[str, str]:
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A"),
    }


TOOL_REGISTRY: dict[str, Callable[..., Any]] = {
    "current_time": get_current_time,
    "add_task": add_task,
    "get_tasks": get_tasks,
    "complete_task": complete_task,
    "add_meeting": add_meeting,
    "get_upcoming_meetings": get_upcoming_meetings,
    "create_reminder": create_reminder,
    "get_reminders": get_reminders,
}

DEFAULT_TOOLS = list(TOOL_REGISTRY)


def create_agent(
    name: str,
    model: str,
    tools: list[str] | None = None,
    instruction: str | None = None,
) -> Agent:
    """Create an ADK agent with a selectable model and tool bundle.

    `model` accepts `gemini`, `claude`, `openai`, or any LiteLLM ID such as
    `openai/gpt-4o-mini`. `tools` contains names from `TOOL_REGISTRY`.
    """
    selected_tools = tools or DEFAULT_TOOLS
    unknown_tools = sorted(set(selected_tools) - TOOL_REGISTRY.keys())
    if unknown_tools:
        available_tools = ", ".join(sorted(TOOL_REGISTRY))
        raise ValueError(
            f"Unknown tools: {', '.join(unknown_tools)}. Available tools: {available_tools}"
        )

    return Agent(
        name=name,
        model=get_model(model),
        description="A personal assistant for tasks, meetings, reminders, and daily planning.",
        instruction=instruction or (
            "You are a helpful personal assistant. Use the available tools when the user "
            "asks to manage tasks, meetings, or reminders. Be concise. Use ISO format "
            "YYYY-MM-DD HH:MM:SS for dates and times."
        ),
        tools=[TOOL_REGISTRY[tool_name] for tool_name in selected_tools],
    )