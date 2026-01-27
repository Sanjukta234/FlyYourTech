
from typing import TypedDict

from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.knowledge_base import knowledge_tool
from tools.leads import lead_management_tool
from tools.scheduler import scheduler_tool

# ----------------------------
# Define State
# ----------------------------

class AgentState(TypedDict):
    input: str
    output: str

# ----------------------------
# Initialize LLM (still used, even if routing is simple)
# ----------------------------

llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash")

# ----------------------------
# Tool Router Node (LangGraph Node)
# ----------------------------

def tool_router(state: AgentState) -> AgentState:
    query = state["input"].lower()

    # Simple routing logic (clear for assignment demo)
    if "lead" in query or "show" in query:
        result = lead_management_tool.run(state["input"])

    elif "meeting" in query or "schedule" in query:
        result = scheduler_tool.run(state["input"])

    else:
        result = knowledge_tool.run(state["input"])

    return {"output": result}

# ----------------------------
# Build LangGraph
# ----------------------------

graph = StateGraph(AgentState)

graph.add_node("router", tool_router)

graph.set_entry_point("router")

graph.add_edge("router", END)

app = graph.compile()

# ----------------------------
# Function used by Flask
# ----------------------------

def run_agent(user_query: str):
    result = app.invoke({"input": user_query})
    return result["output"]