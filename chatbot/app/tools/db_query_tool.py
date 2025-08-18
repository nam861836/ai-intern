from factories.db_factory import DBFactory
from langchain.tools import tool

@tool
def db_query(query: str) -> str:
    """
    Tool to query in DB
    """
    agent = DBFactory.create_sql_agent()
    result = agent.invoke({"input": query})
    return str(result)
