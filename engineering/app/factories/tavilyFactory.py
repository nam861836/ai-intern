from langchain_tavily import TavilySearch
from config.base_config import BaseConfiguration

config = BaseConfiguration()

class SearchFactory:
    _tavily_instance = None

    @classmethod
    def get_tavily(cls):
        if cls._tavily_instance is None:
            cls._tavily_instance = TavilySearch(
                max_results=1,
                search_depth="advanced",
                include_answer=True,
                include_raw_content=True,
                api_key=config.tavily_config.api_key.get_secret_value(),
                description=(
                    "A search engine optimized for comprehensive, accurate, and trusted results. "
                    "Useful for when you need to answer questions about current events. "
                    "Input should be a search query."
                )
            )
        return cls._tavily_instance

