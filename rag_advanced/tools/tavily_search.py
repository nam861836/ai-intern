from langchain_tavily import TavilySearch
from config import tavily_api_key
from langchain_core.tools import tool


search_tool = TavilySearch(
    max_results=1,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    api_key=tavily_api_key,
    description = "A search engine optimized for comprehensive, accurate, and trusted results. Useful for when you need to answer questions about current events. Input should be a search query."  
)

@tool
def tavily_search_tool(query: str) -> str:
    """
    Tool to search web using Tavily
    """
    #query = state["messages"]
    result = search_tool.invoke(query)
    return str(result)
