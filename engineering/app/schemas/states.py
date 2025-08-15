from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    output: str

