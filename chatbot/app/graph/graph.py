from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver
from schemas.states import GraphState
from tools.tavily_search_tool import tavily_search_tool
from tools.db_query_tool import db_query
from tools.rag_tool import RAG
from graph.nodes.supervisor import supervisor_node, should_continue

# from pymongo import MongoClient
from langgraph.checkpoint.mongodb import MongoDBSaver
from services.mongodb import get_mongo_client


def create_supervisor_graph():
    client = get_mongo_client()
    if not client:
        raise ValueError("Failed to create MongoDB client")

    checkpointer = MongoDBSaver(client)
    #checkpointer = InMemorySaver()
    
    builder = StateGraph(GraphState)
    
    # ToolNode with all tools
    tool_node = ToolNode([tavily_search_tool, db_query, RAG])
    
    # Add nodes
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("tools", tool_node)
    
    # Add edges
    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    builder.add_edge("tools", "supervisor")
    
    return builder.compile(checkpointer=checkpointer)

