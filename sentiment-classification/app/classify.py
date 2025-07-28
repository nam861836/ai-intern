import os
from langchain_openai import ChatOpenAI
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough



from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]
model = os.environ["OPENAI_MODEL"]
temperature = os.environ["TEMPERATURE"]

tagging_prompt = ChatPromptTemplate.from_template(
"""
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Passage:
{input}
"""
)

class Classification(BaseModel):
    sentiment: Optional[str] = Field(enum=["positive", "neutral", "negative"])

llm = ChatOpenAI(model=model, temperature=temperature).with_structured_output(schema= Classification)
tagging_chain = tagging_prompt | llm

trump_follower = "I'm confident that President Trump's leadership and track record will once again resonate with Americans. His strong stance on economic growth and national security is exactly what our country needs at this pivotal moment. We need to bring back the proven leadership that can make America great again!"
print(tagging_chain.invoke({"input": trump_follower}))


