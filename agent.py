from typing import Annotated, List
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool, InjectedToolCallId
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import START, StateGraph
from langgraph.types import Command
from langgraph.prebuilt import tools_condition, ToolNode, InjectedState
from dotenv import load_dotenv
from pydantic import BaseModel
from langgraph.graph import MessagesState
from davia import Davia
import operator

load_dotenv()

app = Davia()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

class ScheduleItem(BaseModel):
    activity: str
    start_time: int
    end_time: int

class LifeCoachState(MessagesState):
    tasks: Annotated[List[str], operator.add]
    tomorrows_schedule: Annotated[List[ScheduleItem], operator.add]


# --- TOOLS ---
@tool
def remove_completed_tasks(
    completed_tasks: List[str],
    state: Annotated[LifeCoachState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId] = ""
) -> Command:
    """Removes all tasks marked as completed from the task list."""
    # Ensure all required state fields exist
    current_tasks = state.get("tasks", [])
    before = len(current_tasks)
    updated_tasks = [t for t in current_tasks if t not in completed_tasks]

    
    return Command(update={
        "tasks": updated_tasks,
        "messages": [
            ToolMessage(
                f"Removed {before - len(updated_tasks)} completed tasks.",
                tool_call_id=tool_call_id
            )
        ]
    })

@tool
def create_new_task(
    task: str,
    state: Annotated[LifeCoachState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId] = ""
) -> Command:
    """Add a new task to the task list."""
    current_tasks = state.get("tasks", [])
    current_tasks.append(task)
    return Command(update={
        "tasks": current_tasks, 
        "messages": [
            ToolMessage(
                f"Task '{task}' added successfully.",
                tool_call_id=tool_call_id
            )
        ]
    })

@tool
def clear_tomorrows_schedule(
    state: Annotated[LifeCoachState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId] = ""
) -> Command:
    """Clear tomorrow's schedule."""
    return Command(update={
        "tomorrows_schedule": [],
        "messages": [
            ToolMessage(
                f"Tomorrow's schedule cleared successfully.",
                tool_call_id=tool_call_id
            )
        ]
    })

@tool
def update_tomorrows_schedule(
    activity: str,
    start_time: int,
    end_time: int,
    state: Annotated[LifeCoachState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId] = ""
) -> Command:
    """Update tomorrow's schedule with the new schedule items."""
    current_schedule = state.get("tomorrows_schedule", [])
    current_schedule.append(ScheduleItem(activity=activity, start_time=start_time, end_time=end_time))
    return Command(update={
        "tomorrows_schedule": current_schedule,
        "messages": [
            ToolMessage(
                f"Tomorrow's schedule updated successfully.",
                tool_call_id=tool_call_id
            )
        ]
    })

# Liste des tools pour ToolNode
TOOLS = [remove_completed_tasks, create_new_task, update_tomorrows_schedule, clear_tomorrows_schedule]


llm_with_tools = llm.bind_tools(TOOLS)

system_prompt = """
You are a friendly AI Life Coach who conducts daily check-ins with the user. Today is {date} ({weekday}).

Your job is to help them reflect on their day, update their task list, and plan for tomorrow. Follow this process step by step:

1. **Review Today:**
   - Greet the user warmly and ask what tasks they completed today.
   - For each task the user says they finished, use the remove_completed_tasks tool to remove it from the list.
   - If the user starts by mentioning tasks they need to do (instead of completed tasks), that's not a problem: skip the completed-tasks step and go straight to adding the mentioned tasks to the task list.

2. **Add New Tasks:**
   - Ask if there are any new tasks or responsibilities to add to the list.
   - If the user mentions a new task, you MUST add every single one using the create_new_task tool. If they specify a time (e.g., "at 3pm"), include that time in the task name (e.g., "Call mom at 3pm").
   - If the user does not mention a time or date for a task, add it to the task list. Then, it is YOUR job as the AI to decide—based on the user's time constraints and the apparent urgency of the task—if it should be scheduled for tomorrow.

3. **Plan Tomorrow:**
   - Ask the user about their commitments or availabilities for tomorrow.
   - Use clear_tomorrows_schedule to clear any previous schedule.
   - For each activity, commitment, or time block the user mentions, you MUST add ALL of them to tomorrow's schedule using update_tomorrows_schedule.
   - Then, review the user's current task list and proactively add ALL tasks that are needed for tomorrow to the schedule, even if the user did not mention them.
   - For tasks that do not have a specific time mentioned, YOU must choose an appropriate time slot for them in the schedule if you determine they should be done tomorrow.
   - Analyse the current date and check if any previously mentioned tasks are due for tomorrow (for example, if a user said a task is for Sunday and tomorrow is Sunday, add it to the schedule).
   - Make sure to include ALL tasks and ALL time constraints, commitments, and availabilities the user provides.

**Important Rules:**
- Always use the appropriate tool for each step. Do not just acknowledge; actually update the state.
- If the user mentions a new task with a time, always include the time in the task name.
- Be friendly, supportive, and conversational throughout.
- Never mention the tools or your internal process to the user.
- After scheduling tomorrow, encourage the user and wish them a good day or restful night.

CURRENT STATE:
- Tasks: {tasks}
- Tomorrow's Schedule: {tomorrows_schedule}
"""

def assistant(state: LifeCoachState):
    messages = state["messages"]
    tasks = state.get("tasks", [])
    tomorrows_schedule = state.get("tomorrows_schedule", [])
    now = datetime.now()
    formatted_prompt = system_prompt.format(
        date=now.strftime("%d/%m/%Y"),
        weekday=now.strftime("%A"),
        tasks=", ".join(tasks),
        tomorrows_schedule=", ".join(str(item) for item in tomorrows_schedule)
    )
    response = llm_with_tools.invoke([SystemMessage(content=formatted_prompt)] + messages)
    return {"messages": [response]}

# --- GRAPH ---
@app.graph
def graph():
    builder = StateGraph(LifeCoachState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(TOOLS))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    return builder.compile()


if __name__ == "__main__":
    app.run()

