import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel, Field

from claude_agent.agent import root_agent as claude_agent
from gemini_agent.agent import root_agent as gemini_agent
from openai_agent.agent import root_agent as openai_agent
from personal_assistant.agent_template import TOOL_REGISTRY


APP_NAME = "personal-assistant-ui"
USER_ID = "web-user"
STATIC_DIR = Path(__file__).parent / "static"

AGENTS = {
    "claude": {"label": "Claude", "agent": claude_agent, "accent": "#e07a5f"},
    "gemini": {"label": "Gemini", "agent": gemini_agent, "accent": "#3d8bfd"},
    "openai": {"label": "OpenAI", "agent": openai_agent, "accent": "#36a77c"},
}

session_service = InMemorySessionService()
runners = {
    key: Runner(
        app_name=f"{APP_NAME}-{key}",
        agent=details["agent"],
        session_service=session_service,
    )
    for key, details in AGENTS.items()
}

app = FastAPI(title="Personal Assistant")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class ChatRequest(BaseModel):
    agent: str = Field(pattern="^(claude|gemini|openai)$")
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = None


@app.get("/", response_class=FileResponse)
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/agents")
async def list_agents() -> dict:
    return {
        "agents": [
            {
                "id": agent_id,
                "label": details["label"],
                "model": details["agent"].model.model,
                "tools": list(TOOL_REGISTRY),
                "accent": details["accent"],
            }
            for agent_id, details in AGENTS.items()
        ]
    }


async def get_or_create_session(agent_id: str, session_id: str | None) -> str:
    app_name = f"{APP_NAME}-{agent_id}"
    if session_id:
        session = await session_service.get_session(
            app_name=app_name, user_id=USER_ID, session_id=session_id
        )
        if session:
            return session.id

    session = await session_service.create_session(
        app_name=app_name, user_id=USER_ID, session_id=str(uuid.uuid4())
    )
    return session.id


@app.post("/api/chat")
async def chat(request: ChatRequest) -> dict:
    session_id = await get_or_create_session(request.agent, request.session_id)
    content = types.Content(role="user", parts=[types.Part(text=request.message)])

    try:
        events = runners[request.agent].run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=content,
        )
        response_parts: list[str] = []
        async for event in events:
            if event.is_final_response() and event.content and event.content.parts:
                response_parts.extend(
                    part.text for part in event.content.parts if part.text
                )
    except Exception as error:
        raise HTTPException(status_code=502, detail=str(error)) from error

    return {"session_id": session_id, "response": "\n".join(response_parts)}
