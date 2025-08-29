import pytest
from langchain_core.tools import tool
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver

from schemas.states import GraphState
from utils import prompts
from factories.llm_factory import LLMFactory  # giả sử bạn đã có


# --- Mock tools ---
@tool
def mock_tavily_tool(query: str) -> str:
    """tavily"""
    return f"Mocked Tavily result for: {query}. Paris is the capital of France."


@tool
def mock_db_tool(query: str) -> List[Dict[str, Any]]:
    """db"""
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


@tool
def mock_rag_tool(document: str) -> str:
    """rag"""
    return f"Mocked RAG answer for document: '{document}'. This is an answer from RAG."


# --- Supervisor node cho test (bind mock tools) ---
def supervisor_node_for_test(state: GraphState):
    llm = LLMFactory.create()
    tools = [mock_tavily_tool, mock_db_tool, mock_rag_tool]

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompts.system_prompt),
        MessagesPlaceholder("messages"),
    ])

    supervisor = prompt | llm.bind_tools(tools)
    response = supervisor.invoke(state["messages"])
    return {"messages": [response]}


# --- should_continue (giữ nguyên) ---
from graph.nodes.supervisor import should_continue


# --- Fixture graph ---
@pytest.fixture
def graph():
    tools = [mock_tavily_tool, mock_db_tool, mock_rag_tool]
    builder = StateGraph(GraphState)
    tool_node = ToolNode(tools)

    builder.add_node("supervisor", supervisor_node_for_test)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        should_continue,
        {"tools": "tools", "end": END},
    )
    builder.add_edge("tools", "supervisor")

    return builder.compile(checkpointer=InMemorySaver())


# --- Config ---
checkpoint_config = {"configurable": {"thread_id": "test"}}


# --- Helper ---
def extract_texts(state: dict) -> str:
    texts = []
    for m in state.get("messages", []):
        content = getattr(m, "content", None)
        if content is not None:
            texts.append(content)
        else:
            texts.append(str(m))
    return " ".join(texts)


# --- Tests ---
def test_search_tool_flow(graph):
    init_state = {
        "messages": [HumanMessage(content="What is the capital of France?")],
        "output": ""
    }

    result = graph.invoke(init_state, config=checkpoint_config)

    assert isinstance(result, dict)
    assert "messages" in result

    texts = extract_texts(result)
    assert "Paris" in texts
    assert "Mocked Tavily result" in texts


def test_db_query_tool_flow(graph):
    init_state = {
        "messages": [HumanMessage(content="SELECT * FROM users LIMIT 1")],
        "output": ""
    }

    result = graph.invoke(init_state, config=checkpoint_config)

    assert isinstance(result, dict)
    assert "messages" in result

    texts = extract_texts(result)
    assert "Alice" in texts
    assert "{'id': 1" in texts or "Alice" in texts


def test_rag_tool_flow(graph):
    init_state = {
        "messages": [HumanMessage(content="Summarize document about AI")],
        "output": ""
    }

    result = graph.invoke(init_state, config=checkpoint_config)

    assert isinstance(result, dict)
    assert "messages" in result

    texts = extract_texts(result)
    assert "RAG" in texts
    assert "Mocked RAG answer" in texts
