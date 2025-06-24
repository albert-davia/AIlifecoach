from mailbox import Message
from typing import Annotated, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool, InjectedToolCallId
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langgraph.graph import START, StateGraph
from langgraph.types import Command
from langgraph.prebuilt import tools_condition, ToolNode
from dotenv import load_dotenv
from langgraph.graph import MessagesState
from langgraph.prebuilt import InjectedState



load_dotenv()

class CustomState(MessagesState):
    custom_field: str

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# --- TOOLS ---
@tool
def add_numbers(
    a: float,
    b: float,
    state: Annotated[CustomState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """Adds two numbers together."""
    return Command(update={
        "custom_field": "MERDE ???",
        # update the message history
        "messages": [
            ToolMessage(
                f"added {a} + {b} = {a + b}",
                tool_call_id=tool_call_id
            )
        ]
    })

@tool
def multiply_numbers(
    a: float,
    b: float,
    ) -> float:
    """Multiplies two numbers together."""
    return a * b

# List of available tools
TOOLS = [add_numbers, multiply_numbers]

# Bind tools to LLM
llm_with_tools = llm.bind_tools(TOOLS)

def assistant(state: CustomState):
    # Append the new AI message to the conversation history
    system_prompt = f"""
    You are a helpful math assistant. You can add and multiply numbers using the available tools.
    When asked to perform calculations, use the appropriate tool (add_numbers or multiply_numbers).
    Be friendly and explain your calculations clearly. please always finish your response with the {state["custom_field"]} value.
    """
    return {"messages": [llm_with_tools.invoke([SystemMessage(content=system_prompt)] + state.get("messages", []))]}



# Create the graph
builder = StateGraph(CustomState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(TOOLS))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")
graph = builder.compile()
