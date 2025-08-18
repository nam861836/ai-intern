from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentType
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from factories.llm_factory import LLMFactory
from config.base_config import BaseConfiguration

class DBFactory:
    @staticmethod
    def create_db():
        db_path = "/home/nam861836/Documents/ai-intern/chatbot/data/user_ticket.db"
        return SQLDatabase.from_uri(f"sqlite:///{db_path}")

    @staticmethod
    def create_sql_agent():
        db = DBFactory.create_db()
        llm = LLMFactory.create()
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        return create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            agent_executor_kwargs={"handle_parsing_errors": True},
        )
