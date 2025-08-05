from typing import TypedDict

class GraphState(TypedDict):
    input: str
    route: str
    output: str

def getStateRoute():
    return lambda state: state["route"]