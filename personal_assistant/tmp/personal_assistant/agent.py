import os

from personal_assistant.agent_template import create_agent


root_agent = create_agent(
    name="personal_assistant",
    model=os.getenv("ASSISTANT_MODEL", "gemini"),
)