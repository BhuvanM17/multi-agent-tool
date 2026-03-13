import os
from typing import Annotated, TypedDict, List, Union

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from .tools import tools

# Load environment variables from root
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Define the state
class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


api_key = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=api_key)
llm_with_tools = llm.bind_tools(tools)

# Define the nodes
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Define the graph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))

# Set the entry point
graph_builder.set_entry_point("chatbot")

# Define routing logic
def route_tools(state: State):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# Add conditional edges
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", END: END}
)

# Add edge from tools back to chatbot
graph_builder.add_edge("tools", "chatbot")

# Compile the graph with memory
memory = MemorySaver()
agent = graph_builder.compile(checkpointer=memory)

def run_agent(input_text: str, thread_id: str = "1"):
    """Run the agent with the given input text."""
    config = {"configurable": {"thread_id": thread_id}}
    
    # We can just use the memory checkpointer properly to manage the state
    # Create the state dictionary starting from the input
    initial_state = {"messages": [HumanMessage(content=input_text)]}
    
    final_content = ""
    try:
        # Run the graph and get the final state
        # The stream method yields dictionary objects for the outputs of nodes as they complete
        # We can just iterate to the end, or use invoke for synchronous execution
        response_state = agent.invoke(initial_state, config)
        
        # The last message in the 'messages' list of the state should be the AI's final answer
        messages = response_state.get("messages", [])
        if messages:
            last_msg = messages[-1]
            if isinstance(last_msg, AIMessage):
                final_content = last_msg.content
    except Exception as e:
        print(f"Error during agent execution: {e}")
        import traceback
        traceback.print_exc()
        
    return final_content or "I processed your request, but there was no explicit textual response."
