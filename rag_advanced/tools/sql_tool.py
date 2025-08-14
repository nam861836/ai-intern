import sys
import os
sys.path.insert(1, '/home/nam861836/Documents/ai-intern/rag_advanced')

from langchain_community.utilities import SQLDatabase
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.chains import LLMChain, create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.agents.agent_types import AgentType
from langchain_core.tools import tool


import config
import prompts

llm = ChatOpenAI(model=config.model, temperature=config.temperature)
#print(config.db_path)
db = SQLDatabase.from_uri(f"sqlite:///{config.db_path}")

def create_agent(db: SQLDatabase):
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_executor_kwargs={"handle_parsing_errors": True},
    )
    return agent

@tool
def db_query(query: str) -> str:
    """
    Tool to query in DB
    """
    #query = state["messages"]
    agent_executor = create_agent(db)
    result = agent_executor.invoke({"input": query})
    #print(type(result))
    return str(result)

