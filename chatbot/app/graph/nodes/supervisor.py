from factories.llm_factory import LLMFactory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from schemas.states import GraphState
from utils import prompts
from tools.tavily_search_tool import tavily_search_tool
from tools.db_query_tool import db_query
from tools.rag_tool import RAG

def create_supervisor():
    """Create supervisor agent with tools bound"""
    llm = LLMFactory.create()
    tools = [tavily_search_tool, db_query, RAG]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompts.system_prompt),
        MessagesPlaceholder("messages"),
    ])
    
    return prompt | llm.bind_tools(tools)

def supervisor_node(state: GraphState):
    """Supervisor node that decides which tools to call or when to end"""
    supervisor = create_supervisor()
    messages = state["messages"]
    response = supervisor.invoke(messages)
    return {"messages": [response]}

def should_continue(state: GraphState):
    """Determine whether to continue with tools or end"""
    messages = state["messages"]
    last_message = messages[-1]
    
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    else:
        return "end"
