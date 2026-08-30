# 🤖 Personal AI Assistant

A personal AI assistant built using **Python**, **Google Agent Development Kit (ADK)**, **Gemini**, and **uv**.

The goal of this project is to create an AI-powered assistant that can help manage daily activities such as:

* 📅 Calendar and meetings
* ⏰ Meeting reminders
* ✅ Daily tasks
* 🔔 Desktop notifications
* 📝 Notes
* 📧 Email assistance
* 💻 Laptop-related tasks
* 🤖 Natural-language interaction

The project will initially use a local SQLite database and can later be extended with Google Calendar, Gmail, MCP, voice interaction, and other integrations.

---

## 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │       USER       │
                         └────────┬─────────┘
                                  │
                                  ▼
                       ┌────────────────────┐
                       │   Personal Agent   │
                       │   Google ADK       │
                       │   Gemini           │
                       └─────────┬──────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             │                   │                   │
             ▼                   ▼                   ▼
       ┌───────────┐       ┌────────────┐      ┌────────────┐
       │   Tasks   │       │  Calendar  │      │ Reminders  │
       │   Tools   │       │   Tools    │      │   Tools    │
       └─────┬─────┘       └──────┬─────┘      └──────┬─────┘
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  ▼
                         ┌─────────────────┐
                         │  SQLite DB      │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Scheduler     │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Desktop Alerts  │
                         └─────────────────┘
```

---

# 📋 Prerequisites

Before starting, make sure the following are installed.

### Required

* Python 3.12+
* uv
* Git
* Google Gemini API Key

Check Python:

```bash
python3 --version
```

Example:

```text
Python 3.12.x
```

Check Git:

```bash
git --version
```

---

# 1. Install uv

`uv` is used to manage:

* Python versions
* Virtual environments
* Project dependencies
* Running Python commands

Install `uv` on macOS/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal.

Verify the installation:

```bash
uv --version
```

Example:

```text
uv 0.x.x
```

---

# 2. Install Python Using uv

Install Python 3.12:

```bash
uv python install 3.12
```

Verify:

```bash
uv python list
```

---

# 3. Create the Project

Create a new project:

```bash
uv init personal-assistant
```

Move into the project:

```bash
cd personal-assistant
```

The initial project will look similar to:

```text
personal-assistant/
├── .python-version
├── pyproject.toml
├── README.md
└── main.py
```

---

# 4. Configure Python Version

Pin Python 3.12 for the project:

```bash
uv python pin 3.12
```

Verify:

```bash
cat .python-version
```

Expected:

```text
3.12
```

---

# 5. Install Google ADK

Install Google Agent Development Kit:

```bash
uv add google-adk
```

---

# 6. Install Additional Dependencies

Install environment-variable support:

```bash
uv add python-dotenv
```

Install scheduler:

```bash
uv add apscheduler
```

Install desktop notifications:

```bash
uv add plyer
```

At this point the project dependencies are managed by `uv`.

You can check them in:

```text
pyproject.toml
```

---

# 7. Create Project Structure

Create the required directories:

```bash
mkdir -p personal_assistant
mkdir -p tools
mkdir -p services
mkdir -p database
```

Create Python package files:

```bash
touch personal_assistant/__init__.py
touch tools/__init__.py
touch services/__init__.py
```

The project should now look like:

```text
personal-assistant/
│
├── .python-version
├── pyproject.toml
├── README.md
├── main.py
│
├── personal_assistant/
│   ├── __init__.py
│   └── agent.py
│
├── tools/
│   ├── __init__.py
│   ├── task_tools.py
│   ├── calendar_tools.py
│   └── reminder_tools.py
│
├── services/
│   ├── __init__.py
│   ├── scheduler.py
│   └── notification_service.py
│
└── database/
```

---

# 8. Create Gemini API Key

The assistant needs access to a Gemini model.

Create a Gemini API key using Google AI Studio.

Then create a `.env` file in the project root:

```text
personal-assistant/
└── .env
```

Add:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Replace:

```text
your_gemini_api_key_here
```

with your actual API key.

---

# 9. Protect the API Key

Never commit `.env` to Git.

Create `.gitignore`:

```bash
touch .gitignore
```

Add:

```gitignore
.env
.venv/
__pycache__/
*.pyc
database/*.db
.DS_Store
```

---

# 10. Create the ADK Agent

Create:

```text
personal_assistant/agent.py
```

The agent will contain:

* Gemini model configuration
* Agent instructions
* Task tools
* Calendar tools
* Reminder tools

Example:

```python
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
    Return current local date and time.
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
    You are a personal AI assistant.

    Help the user manage:

    - Daily tasks
    - Meetings
    - Calendar activities
    - Reminders
    - Daily planning

    Always use the available tools when the user
    wants to create, retrieve, update or manage
    tasks, meetings or reminders.

    Be concise and helpful.

    When working with dates and times use:

    YYYY-MM-DD HH:MM:SS
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
```

---

# 11. Create Task Tools

Create:

```text
tools/task_tools.py
```

The task tools will eventually provide functionality such as:

```text
add_task()
get_tasks()
complete_task()
delete_task()
update_task()
```

Example user interaction:

```text
User:

Add a task to complete API automation today.
```

The ADK agent determines that it needs to call:

```python
add_task()
```

---

# 12. Create Calendar Tools

Create:

```text
tools/calendar_tools.py
```

Initial functionality:

```text
add_meeting()
get_upcoming_meetings()
```

Example:

```text
User:

Schedule a project meeting tomorrow at 10 AM.
```

The agent calls:

```python
add_meeting()
```

Later this will be replaced/extended with **Google Calendar API integration**.

---

# 13. Create Reminder Tools

Create:

```text
tools/reminder_tools.py
```

Initial functionality:

```text
create_reminder()
get_reminders()
```

Example:

```text
User:

Remind me to call my manager at 5 PM.
```

The agent stores the reminder.

---

# 14. Initialize the Database

The application will use SQLite for local storage.

The database will eventually contain:

```text
tasks
meetings
reminders
notes
```

Create:

```text
init_db.py
```

Run:

```bash
uv run python init_db.py
```

The database will be created under:

```text
database/assistant.db
```

---

# 15. Verify Dependencies

Run:

```bash
uv sync
```

This ensures that all dependencies defined in `pyproject.toml` are installed.

You can also check:

```bash
uv tree
```

This displays the project's dependency tree.

---

# 16. Run the Agent from CLI

Run:

```bash
uv run adk run personal_assistant
```

You should then be able to interact with the agent from the terminal.

Example:

```text
You:

What time is it?

Assistant:

The current time is ...
```

---

# 17. Run the ADK Web Interface

For development, the ADK web interface is very useful.

Run:

```bash
uv run adk web
```

ADK will start its development server.

The terminal will display the local URL.

Open that URL in your browser.

You should see the ADK development interface.

Select:

```text
personal_assistant
```

and start chatting with your agent.

---

# 18. Test the Agent

Try these commands.

### Test 1 — Current time

```text
What is the current date and time?
```

---

### Test 2 — Add task

```text
Add a task to complete the API automation project.
```

---

### Test 3 — View tasks

```text
Show me my pending tasks.
```

---

### Test 4 — Complete task

```text
Mark task 1 as completed.
```

---

### Test 5 — Add meeting

```text
Schedule a project meeting tomorrow at 10 AM.
```

---

### Test 6 — Upcoming meetings

```text
What meetings do I have coming up?
```

---

### Test 7 — Reminder

```text
Remind me to call my manager tomorrow at 5 PM.
```

---

# 19. Automatic Desktop Notifications

The next stage is to run a background scheduler.

The architecture will be:

```text
             SQLite
                │
                ▼
        ┌───────────────┐
        │   Scheduler   │
        │               │
        │ Every 30 sec  │
        └───────┬───────┘
                │
                ▼
       Check upcoming reminder
                │
                ▼
        ┌───────────────┐
        │   Notification│
        │    Service    │
        └───────┬───────┘
                │
                ▼
          🔔 Desktop Alert
```

Example:

```text
🔔 Meeting Reminder

Project Kickoff starts in 15 minutes.
```

---

# 20. Google Calendar Integration

After the local calendar works, integrate Google Calendar.

The final flow will become:

```text
User
 │
 ▼
ADK Agent
 │
 ▼
Calendar Tool
 │
 ▼
Google Calendar API
 │
 ▼
Your real calendar
```

Example:

```text
User:

What meetings do I have tomorrow?
```

The agent will retrieve the actual Google Calendar events.

Example response:

```text
You have 3 meetings tomorrow:

09:30 AM
Daily Standup

11:00 AM
Project Discussion

03:00 PM
Client Meeting
```

---

# 21. Future Gmail Integration

The assistant can later integrate Gmail.

Example:

```text
User:

Do I have any important emails today?
```

The agent can retrieve relevant emails and summarize them.

Another example:

```text
User:

Summarize today's emails.
```

Architecture:

```text
              ADK Agent
                  │
          ┌───────┴────────┐
          │                │
          ▼                ▼
     Calendar Tool     Gmail Tool
          │                │
          ▼                ▼
   Google Calendar       Gmail
```

---

# 22. Laptop Automation

Eventually, we can add controlled laptop tools.

Possible functionality:

```text
Open Chrome
Open VS Code
Open Terminal
Open a project
Open a website
Create a file
Search local files
Run approved commands
```

Example:

```text
User:

Open my personal assistant project in VS Code.
```

The agent could invoke a controlled tool such as:

```python
open_project()
```

For security, arbitrary shell execution should **not** be exposed directly to the LLM. Use allowlisted operations and require confirmation for potentially destructive actions.

---

# 23. Voice Assistant

A later version can support:

```text
🎤 User speaks
       │
       ▼
Speech-to-Text
       │
       ▼
ADK Agent
       │
       ▼
Tools
       │
       ▼
Text-to-Speech
       │
       ▼
🔊 Assistant speaks
```

Example:

```text
You:

"Hey assistant, what meetings do I have today?"

Assistant:

"You have three meetings today..."
```

---

# 24. Recommended Agent Architecture

As the project becomes larger, use specialized agents.

```text
                       ┌───────────────────┐
                       │   Root Agent      │
                       │ Personal Assistant│
                       └─────────┬─────────┘
                                 │
          ┌──────────────────────┼─────────────────────┐
          │                      │                     │
          ▼                      ▼                     ▼
   ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
   │ Task Agent  │       │Calendar Agent│      │Reminder Agent│
   └──────┬──────┘       └──────┬──────┘       └──────┬──────┘
          │                     │                     │
          ▼                     ▼                     ▼
      Task DB              Google Calendar       Scheduler
```

The root agent decides which specialized agent/tool should handle the request.

---

# 25. Development Workflow

Whenever you start working on the project:

```bash
cd personal-assistant
```

Synchronize dependencies:

```bash
uv sync
```

Run the ADK development UI:

```bash
uv run adk web
```

Make your code changes.

Test the agent.

---

# 26. Git Setup

Initialize Git:

```bash
git init
```

Add files:

```bash
git add .
```

Create your first commit:

```bash
git commit -m "Initial personal AI assistant project"
```

Before committing, verify that `.env` is ignored:

```bash
git status
```

You should **not** see:

```text
.env
```

---

# 27. Useful uv Commands

### Check uv version

```bash
uv --version
```

### List installed Python versions

```bash
uv python list
```

### Install Python

```bash
uv python install 3.12
```

### Pin Python

```bash
uv python pin 3.12
```

### Add dependency

```bash
uv add package-name
```

Example:

```bash
uv add google-adk
```

### Remove dependency

```bash
uv remove package-name
```

### Synchronize environment

```bash
uv sync
```

### Run Python

```bash
uv run python
```

### Run Python file

```bash
uv run python init_db.py
```

### Run ADK

```bash
uv run adk web
```

---

# 28. Complete Setup Commands

For a fresh machine, the basic setup is:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python
uv python install 3.12

# Create project
uv init personal-assistant

# Enter project
cd personal-assistant

# Pin Python
uv python pin 3.12

# Install dependencies
uv add google-adk
uv add python-dotenv
uv add apscheduler
uv add plyer

# Create directories
mkdir -p personal_assistant
mkdir -p tools
mkdir -p services
mkdir -p database

# Create package files
touch personal_assistant/__init__.py
touch tools/__init__.py
touch services/__init__.py

# Synchronize environment
uv sync

# Run ADK
uv run adk web
```

---

# 29. Final Project Structure

The completed project is expected to look like:

```text
personal-assistant/
│
├── .env
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
├── uv.lock
│
├── personal_assistant/
│   ├── __init__.py
│   ├── agent.py
│   │
│   └── agents/
│       ├── task_agent.py
│       ├── calendar_agent.py
│       ├── reminder_agent.py
│       └── laptop_agent.py
│
├── tools/
│   ├── __init__.py
│   ├── task_tools.py
│   ├── calendar_tools.py
│   ├── reminder_tools.py
│   ├── gmail_tools.py
│   └── laptop_tools.py
│
├── services/
│   ├── __init__.py
│   ├── scheduler.py
│   └── notification_service.py
│
├── database/
│   └── assistant.db
│
└── tests/
    ├── test_tasks.py
    ├── test_calendar.py
    └── test_reminders.py
```

---

# 🚀 Development Roadmap

## Phase 1 — Basic Agent

* [x] Python project
* [x] uv setup
* [x] Google ADK
* [x] Gemini model
* [ ] Basic agent testing

## Phase 2 — Task Management

* [ ] Add task
* [ ] List tasks
* [ ] Complete task
* [ ] Delete task
* [ ] Update task
* [ ] Task priorities

## Phase 3 — Reminders

* [ ] Create reminder
* [ ] List reminders
* [ ] Background scheduler
* [ ] Desktop notification
* [ ] Meeting reminder

## Phase 4 — Calendar

* [ ] Local calendar
* [ ] Google Calendar API
* [ ] Create event
* [ ] Update event
* [ ] Delete event
* [ ] Today's meetings
* [ ] Tomorrow's meetings

## Phase 5 — Gmail

* [ ] Gmail API
* [ ] Read emails
* [ ] Summarize emails
* [ ] Find important emails

## Phase 6 — Laptop Assistant

* [ ] Open applications
* [ ] Open websites
* [ ] Open projects
* [ ] Search files
* [ ] Controlled terminal commands

## Phase 7 — Voice

* [ ] Speech-to-text
* [ ] Voice commands
* [ ] Text-to-speech
* [ ] Wake word

## Phase 8 — Advanced ADK

* [ ] Multi-agent architecture
* [ ] Agent delegation
* [ ] Session management
* [ ] Persistent memory
* [ ] MCP integration
* [ ] Authentication
* [ ] Logging
* [ ] Error handling
* [ ] Automated tests

---

# 🎯 Example Final Experience

Eventually, you should be able to open your laptop and say:

```text
You:

Good morning.
```

The assistant:

```text
Good morning!

Here is your schedule for today:

📅 Meetings
09:30 AM - Daily Standup
11:00 AM - Project Discussion
03:00 PM - Client Meeting

✅ Tasks
1. Complete API automation
2. Review pull request
3. Update documentation

⏰ Reminders
05:00 PM - Call manager

You have 3 meetings and 3 pending tasks today.
```

And during the day:

```text
🔔 15-minute reminder

Client Meeting starts at 3:00 PM.
```

The long-term goal is to turn this into a **personal AI operating assistant** that can understand natural-language requests and safely perform approved actions across your calendar, reminders, email, and laptop.
