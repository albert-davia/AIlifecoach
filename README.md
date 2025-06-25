# AI Life Coach

An intelligent life coaching agent that helps you manage your daily tasks and schedule. Built with LangGraph and Davia.

## What it does

The AI Life Coach conducts daily check-ins to help you:
- Review completed tasks from your day
- Add new tasks to your schedule
- Organize your schedule intelligently with conflict-free time slots
- Use military time format (0000-2359) for precise scheduling

The agent automatically:
- Avoids scheduling conflicts
- Estimates task duration when only start time is provided
- Works around your specified time constraints
- Prioritizes urgent tasks

## Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up environment

Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the app

```bash
python agent.py
```


## How it works

The app uses Davia's `@app.graph` decorator to create a LangGraph-based conversational agent:

```python
from davia import Davia

app = Davia()

@app.graph
def graph():
    # LangGraph configuration
    builder = StateGraph(LifeCoachState)
    # ... graph setup
    return builder.compile()

if __name__ == "__main__":
    app.run()
```

## Usage

1. Start the application
2. The AI will greet you and ask about completed tasks
3. Add new tasks with or without specific times
4. The agent will organize your schedule automatically
5. All times are handled in military format (0000-2359)

## Project Structure

```
AIlifecoach/
├── agent.py                 # Main application
├── requirements.txt         # Dependencies
├── langgraph.json          # LangGraph configuration
└── README.md               # This file
```
