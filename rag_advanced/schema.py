from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, ToolMessage
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    output: str
    #next_action: str

def getStateRoute():
    return lambda state: state["route"]