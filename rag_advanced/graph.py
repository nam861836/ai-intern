from langgraph.graph import StateGraph
from schema import GraphState
from router_node import route_query
from tools.tavily_search import tavily_search_tool
from tools.sql_tool import db_query
from tools.vectordb_tool import RAG
from langgraph.graph import END, START, StateGraph



def create_langgraph():
    builder = StateGraph(GraphState)

    builder.add_node("router", route_query)
    builder.add_node("sql_tool", db_query)
    builder.add_node("tavily_tool", tavily_search_tool)
    builder.add_node("vectordb_tool", RAG)

    builder.add_edge(START, "router")

    builder.add_conditional_edges("router", lambda state: state["route"], {
        "sql": "sql_tool",
        "tavily": "tavily_tool",
        "vectordb": "vectordb_tool"
    })

    builder.add_edge("sql_tool", END)
    builder.add_edge("tavily_tool", END)
    builder.add_edge("vectordb_tool", END)

    return builder.compile()