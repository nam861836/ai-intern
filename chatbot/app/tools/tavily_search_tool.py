from factories.tavily_factory import SearchFactory
from langchain.tools import tool

@tool
def tavily_search_tool(query: str) -> str:
    """
    Tool to search web using Tavily
    """
    search_tool = SearchFactory.get_tavily()
    result = search_tool.invoke(query)
    return str(result)
