from langgraph.graph import StateGraph
from schema import GraphState
from router_node import route_query
from tools.tavily_search import tavily_search_tool
from tools.sql_tool import db_query
from tools.vectordb_tool import RAG
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
import config, prompts
from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder



#tools = [tavily_search_tool, db_query, RAG]  # Thêm các tool khác của bạn
#tool_node = ToolNode(tools)
llm = ChatOpenAI(model=config.model, temperature=config.temperature)

def create_supervisor():
    """Create supervisor agent with tools bound"""
    llm = ChatOpenAI(model=config.model, temperature=config.temperature)
    
    tools = [tavily_search_tool, db_query, RAG]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompts.supervisor_prompt),
        MessagesPlaceholder("messages"),
    ])
    
    return prompt | llm.bind_tools(tools)

def supervisor_node(state: GraphState):
    """Supervisor node that decides which tools to call or when to end"""
    supervisor = create_supervisor()
    messages = state["messages"]
    
    response = supervisor.invoke(messages)
    return {"messages": [response]}

def should_continue(state: GraphState) -> Literal["tools", "end"]:
    """Determine whether to continue with tools or end"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the last message has tool calls, go to tools
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    else:
        return "end"

tool_node = ToolNode([tavily_search_tool, db_query, RAG])

def create_supervisor_graph():
    """Create the supervisor graph"""
    # Create the graph
    builder = StateGraph(GraphState)
    
    # Add nodes
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("tools", tool_node)
    
    # Add edges
    builder.add_edge(START, "supervisor")
    
    # Add conditional edges from supervisor
    builder.add_conditional_edges(
        "supervisor",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    
    # Add edge from tools back to supervisor
    builder.add_edge("tools", "supervisor")
    
    return builder.compile()