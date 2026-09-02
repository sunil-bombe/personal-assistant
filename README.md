# Personal Assistant

A local, web-based personal assistant powered by Google ADK and LiteLLM. Choose
Claude, Gemini, or OpenAI before starting a conversation. Every provider uses
the same agent template, SQLite-backed tools, and private in-memory web
sessions.

## Features

- Agent picker for Claude, Gemini, and OpenAI.
- Separate conversation session for each selected provider.
- Task management: add, list, and complete tasks.
- Calendar management: add and list upcoming meetings.
- Reminders: create and list pending reminders.
- Current date and time tool.
- Responsive desktop and mobile web interface.
- Custom model IDs supported through LiteLLM.
- Tool selection supported when creating agents in Python.

## Project Structure

```text
personal-assistant/
├── main.py                         # Custom web server entrypoint
├── run.sh                          # Step-by-step setup and launch script
├── web_app.py                      # FastAPI app and ADK runner integration
├── init_db.py                      # Initialize the SQLite database
├── pyproject.toml                  # uv project configuration
├── requirements.txt                # pip dependencies
├── database/assistant.db           # Local SQLite database
├── static/
│   ├── index.html                  # Web UI markup
│   ├── styles.css                  # Responsive visual design
│   └── app.js                      # Agent picker and chat client
├── personal_assistant/
│   ├── agent.py                    # Default configurable ADK agent
│   ├── agent_template.py           # Agent factory and tool registry
│   ├── model_config.py             # LiteLLM provider configuration
│   ├── claude_agent.py             # Claude agent definition
│   ├── gemini_agent.py             # Gemini agent definition
│   └── openai_agent.py             # OpenAI agent definition
├── claude_agent/agent.py           # Standalone ADK app entrypoint
├── gemini_agent/agent.py           # Standalone ADK app entrypoint
├── openai_agent/agent.py           # Standalone ADK app entrypoint
└── tools/
    ├── task_tools.py
    ├── calendar_tools.py
    └── reminder_tools.py
```

## Requirements

- macOS, Linux, or Windows
- Python 3.12 or newer
- `uv` recommended, or Python `venv` and `pip`
- An API key for the provider you want to use

The project uses `google-adk[extensions]`, which includes the LiteLLM
integration needed for Claude, Gemini, and OpenAI models.

## Installation With uv

From the project directory:

```bash
cd personal-assistant
uv sync
```

The first synchronization installs the ADK, LiteLLM, FastAPI, Uvicorn, and
related dependencies into the project environment.

## Installation With pip

```bash
cd personal-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Environment Configuration

Create a local `.env` file in the project root. Add only the keys required by
the provider you plan to use:

```dotenv
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
```

Gemini also accepts `GOOGLE_API_KEY` and
`GOOGLE_GENERATIVE_AI_API_KEY`; the application maps those names to
`GEMINI_API_KEY` when needed.

Never commit real API keys. The `.gitignore` should include `.env` in addition
to the virtual environment and generated Python files.

## Start The Custom Web UI

Initialize the database once:

```bash
uv run python init_db.py
```

Start the custom web interface:

```bash
uv run python main.py
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080) in a browser, select an
agent, and then start chatting.

If port `8080` is already in use, choose another port with `PORT`:

```bash
PORT=8081 uv run python main.py
```

The host is configurable too:

```bash
HOST=0.0.0.0 PORT=8081 uv run python main.py
```

The server reads `HOST` and `PORT` in [main.py](main.py). The default values are
`127.0.0.1` and `8080`.

## Run With The Script

On macOS or Linux, the included [run.sh](run.sh) performs the setup and launch
steps in order:

1. Finds the project directory, regardless of the current shell directory.
2. Checks that `uv` is installed.
3. Synchronizes dependencies with `uv sync`.
4. Initializes the SQLite database with `init_db.py`.
5. Compiles the application and tool modules.
6. Starts the custom web UI.

Make the script executable once:

```bash
chmod +x run.sh
```

Run it from the project directory:

```bash
./run.sh
```

The script resolves its own project directory, so it can also be started from
another directory with its absolute path:

```bash
/Users/your-name/path/to/personal-assistant/run.sh
```

The runner does not create `.env` or API keys. Create `.env` first and add the
credentials for the provider you want to use, as described in
[Environment Configuration](#environment-configuration). Without a valid key,
the page will load but model requests will fail authentication.

Open the printed URL, select an agent, and begin chatting. Press `Ctrl+C` in
the terminal to stop the server.

If port `8080` is occupied, pass a different port:

```bash
PORT=8081 ./run.sh
```

To listen on a specific host and port:

```bash
HOST=0.0.0.0 PORT=8081 ./run.sh
```

The script prints the active project directory and URL, then runs these
commands in order:

```text
Step 1/4: uv sync
Step 2/4: uv run python init_db.py
Step 3/4: uv run python -m py_compile ...
Step 4/4: uv run python main.py
```

It stops immediately if dependency installation, database initialization,
compilation, or server startup fails. Press `Ctrl+C` to stop the final server
step.

## Using The Web UI

1. Open the web UI.
2. Select Claude, Gemini, or OpenAI from the agent cards.
3. Confirm the displayed model and tool count.
4. Use a suggestion or type a message.
5. Press Enter to send. Use Shift + Enter for a new line.
6. Select **New chat** to clear the current conversation and create a fresh
   session.

The UI calls these endpoints:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Serves the web interface |
| `GET` | `/api/agents` | Lists selectable agents, models, and tools |
| `POST` | `/api/chat` | Sends a message to the selected agent |

Example chat request:

```bash
curl -X POST http://127.0.0.1:8080/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"agent":"gemini","message":"Show my upcoming meetings"}'
```

The response includes a `session_id`. Send it with later requests to continue
the same provider-specific conversation.

## Available Agents

The custom UI exposes these agents:

| UI ID | Model alias | Default model |
| --- | --- | --- |
| `claude` | `claude` | `anthropic/claude-sonnet-4-20250514` |
| `gemini` | `gemini` | `gemini/gemini-2.5-flash` |
| `openai` | `openai` | `openai/gpt-5.4-mini` |

The standalone ADK app entrypoints are also available in `claude_agent/`,
`gemini_agent/`, and `openai_agent/`. To run the ADK development UI instead of
the custom interface:

```bash
uv run adk web --port 8001
```

ADK Web will discover the standalone apps and the original
`personal_assistant` app. Use port `8001` if port `8000` is occupied.

## Create A Custom Agent

Use [agent_template.py](personal_assistant/agent_template.py) when you need a
different model or a smaller tool bundle:

```python
from personal_assistant.agent_template import create_agent

planning_agent = create_agent(
    name="planning_agent",
    model="claude",
    tools=["current_time", "add_task", "get_tasks"],
)
```

`model` accepts `gemini`, `claude`, `openai`, or any provider-qualified LiteLLM
ID such as `openai/gpt-4o-mini`.

Available tool names:

```text
current_time
add_task
get_tasks
complete_task
add_meeting
get_upcoming_meetings
create_reminder
get_reminders
```

An unknown tool name raises a clear `ValueError`. If `tools` is omitted, the
agent receives the complete default tool bundle.

## Model Configuration

The default configurable agent reads `ASSISTANT_MODEL` from `.env`:

```dotenv
ASSISTANT_MODEL=gemini
```

You can use an alias:

```dotenv
ASSISTANT_MODEL=claude
```

Or a complete LiteLLM model ID:

```dotenv
ASSISTANT_MODEL=openai/gpt-4o-mini
```

The three UI agent cards use fixed aliases so selecting an agent always selects
the intended provider. Change the defaults in
[model_config.py](personal_assistant/model_config.py) when you want to update
the model behind an alias.

## Database Tools

The SQLite database is stored at `database/assistant.db`. Initialize it with:

```bash
uv run python init_db.py
```

The tool modules create their tables when their initialization functions run.
For a clean local database, stop the app, remove `database/assistant.db`, and
run the initialization command again.

## Testing And Validation

Compile the application and tools:

```bash
uv run python -m py_compile \
  main.py web_app.py init_db.py \
  personal_assistant/*.py \
  claude_agent/agent.py gemini_agent/agent.py openai_agent/agent.py \
  tools/*.py
```

Check the custom web server without making a model request:

```bash
PORT=8081 uv run python main.py
```

In another terminal:

```bash
curl http://127.0.0.1:8081/api/agents
curl http://127.0.0.1:8081/
```

The agent endpoint should return Claude, Gemini, and OpenAI. A real chat request
requires a valid API key for the selected provider and may incur provider
charges.

## Troubleshooting

### Address already in use

Run the custom UI on another port:

```bash
PORT=8081 uv run python main.py
```

To see what is using a port on macOS:

```bash
lsof -i :8080
```

### LiteLLM import error

Install the ADK extensions and synchronize the environment:

```bash
uv sync
```

For pip installations, reinstall from `requirements.txt`.

### Provider authentication error

Check that the selected provider's environment variable is present in `.env`
and that the key is valid. Restart the server after changing `.env`.

### Gemini LiteLLM warning

ADK may warn that Gemini's native integration can be used directly. This is an
informational warning; the current implementation intentionally uses LiteLLM
so all three providers share the same model interface.
