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

class Task(BaseModel):
    name: str
    timeslot: tuple[int, int]
    add_or_remove_flag: bool

def custom_reduce(left: List[Task], right: List[Task]) -> List[Task]:
    for task in right:
        if task.add_or_remove_flag:
            left.append(task)
        else:
            left = [t for t in left if t.name != task.name or t.timeslot != task.timeslot]
    return left



class LifeCoachState(MessagesState):
    tasks: Annotated[List[Task], custom_reduce]


# --- TOOLS ---
@tool
def remove_completed_task(
    task: str,
    start_time: int,
    end_time: int,
    tool_call_id: Annotated[str, InjectedToolCallId] = ""
) -> Command:
    """Removes all tasks marked as completed from the task list."""
    # Ensure all required state fields exist
    removed_task = Task(name=task, add_or_remove_flag=False, timeslot=(start_time, end_time))
    return Command(update={
        "tasks": [removed_task],
        "messages": [
            ToolMessage(
                f"Removed {task} from the task list.",
                tool_call_id=tool_call_id
            )
        ]
    })

@tool
def create_new_task(
    task: str,
    start_time: int,
    end_time: int,
    tool_call_id: Annotated[str, InjectedToolCallId] = ""
) -> Command:
    """Add a new task to the task list."""
    new_task = Task(name=task, add_or_remove_flag=True, timeslot=(start_time, end_time))
    return Command(update={
        "tasks": [new_task], 
        "messages": [
            ToolMessage(
                f"Task '{task}' added successfully.",
                tool_call_id=tool_call_id
            )
        ]
    })



# Liste des tools pour ToolNode
TOOLS = [remove_completed_task, create_new_task]


llm_with_tools = llm.bind_tools(TOOLS)

system_prompt = """ You are a friendly AI Life Coach who conducts daily check-ins with the user. Today is {date} ({weekday}).

Your job is to help them reflect on their day, update their task list, and organize their schedule intelligently. You have two main functions: adding new tasks and removing completed tasks.

**IMPORTANT: Always use military time format (0000 to 2359) for all time specifications.**

Follow this process step by step:

1. **Review Today:**
   - Greet the user warmly and ask what tasks they completed today.
   - For each task the user says they finished, use the remove_completed_task tool to remove it from the list.
   - If the user starts by mentioning tasks they need to do (instead of completed tasks), that's not a problem: skip the completed-tasks step and go straight to adding the mentioned tasks to the task list.

2. **Add New Tasks & Organize Schedule:**
   - Ask if there are any new tasks or responsibilities to add to the list.
   - If the user mentions a new task, you MUST add every single one using the create_new_task tool.
   - **Time Slot Management:**
     - If the user specifies a time slot (e.g., "at 3pm", "from 2-4pm"), NEVER change it. Work around their schedule.
     - If the user only specifies a starting time (e.g., "at 3pm"), estimate the task duration yourself based on the task type and add an appropriate end time.
     - If the user doesn't specify any time, YOU must decide when it should be scheduled based on urgency, task type, and available time slots.
     - NEVER schedule two tasks in the same time slot. If there's a conflict, find the next available time slot.
     - Consider task priority, duration, and dependencies when scheduling.
     - **Always convert times to military format (e.g., 3pm = 1500, 2am = 0200, 11:30am = 1130).**

3. **Schedule Organization Rules:**
   - Always check for time conflicts before adding new tasks.
   - For tasks without specified times, prioritize urgent tasks and schedule them earlier in the day.
   - Estimate task duration based on task type (e.g., "Call mom" = 30 minutes, "Write report" = 2 hours, "Exercise" = 1 hour).
   - If a user-specified time conflicts with existing tasks, find the next available slot and inform the user.
   - Be proactive about scheduling tasks that are due soon or are important.

**Important Rules:**
- Always use the appropriate tool for each step. Do not just acknowledge; actually update the state.
- If the user mentions a new task with a time, always include the time in the task name.
- Be friendly, supportive, and conversational throughout.
- Never mention the tools or your internal process to the user.
- After organizing the schedule, encourage the user and wish them a good day or restful night.
- Always maintain a conflict-free schedule by checking existing time slots before adding new tasks.
- **Use military time format (0000-2359) for all time inputs to the tools.**
- **If you need to modify a task (change time, name, etc.), first remove it using remove_completed_task, then add the modified version using create_new_task.**

CURRENT STATE:
- Tasks: {tasks}
"""

def assistant(state: LifeCoachState):
    messages = state["messages"]
    tasks = state.get("tasks", [])
    now = datetime.now()
    formatted_prompt = system_prompt.format(
        date=now.strftime("%d/%m/%Y"),
        weekday=now.strftime("%A"),
        tasks=", ".join([task.name for task in tasks if task.add_or_remove_flag])
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
    return builder


if __name__ == "__main__":
    app.run()