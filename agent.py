from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import tools_list
import os
from langchain_core.messages import SystemMessage

# 1. Define the State
# This 'messages' list will store the whole conversation, including tool outputs.
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Initialize the Model and "Bind" the Tools
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=os.getenv("GEMINI_API_KEY")
)
# This tells Gemini: "You have permission to use these Python functions"
model_with_tools = llm.bind_tools(tools_list)

# 3. Define the Nodes
def call_model(state: AgentState):
    """The brain node: Decides what to do next."""
    messages = state['messages']
    
    # Define the professional, end-user oriented persona
    system_prompt = SystemMessage(content=(
        "You are 'ThreatLens AI', an elite cybersecurity analyst designed for common users. "
        "Your goal is to investigate emails and provide clear, non-technical safety verdicts. "
        "\n\nRULES:\n"
        "1. Use the 'check_domain_age' and 'scan_url' tools to gather evidence.\n"
        "2. If a domain is malicious, use 'draft_takedown_report' to prepare a response.\n"
        "3. FINAL RESPONSE: Do not show raw JSON, signatures, or technical tool names. "
        "Instead of 'WHOIS check failed', say 'We couldn't find a registered owner for this site.' "
        "Use bold text for safety warnings and keep your tone helpful yet firm."
    ))
    
    # Prepend the system prompt to the message list
    response = model_with_tools.invoke([system_prompt] + messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    """The logic edge: Checks if the model wants to use a tool."""
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "continue"
    return "end"

# 4. Build the Graph
workflow = StateGraph(AgentState)

# Add our nodes
workflow.add_node("agent", call_model)

# Prebuilt tool executor from LangGraph
from langgraph.prebuilt import ToolNode
tool_node = ToolNode(tools_list)
workflow.add_node("action", tool_node)

# Set the Entry Point
workflow.set_entry_point("agent")

# Add Conditional Edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END
    }
)

# Add a normal edge: After 'action', always go back to 'agent' to think
workflow.add_edge("action", "agent")

# Compile the Graph
threat_lens_agent = workflow.compile()