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

def extract_sql(text: str) -> str:
    # Safely extract the SQL query from the LLM response
    for line in text.splitlines():
        if line.startswith("SQLQuery:"):
            return line.replace("SQLQuery:", "").strip()
    return text  # fallback


llm = ChatOpenAI(model=model, temperature=temperature)

sqlite_db_path = "../data/street_tree_db.sqlite"

db = SQLDatabase.from_uri(f"sqlite:///{sqlite_db_path}")

write_query = create_sql_query_chain(llm, db)

execute_query = QuerySQLDataBaseTool(db=db)

'''
for line in response.splitlines():
    if line.startswith("SQLQuery:"):
        sql_query = line.replace("SQLQuery:", "").strip()
        break
'''
#print(sql_query)

#print(db.run(sql_query))

#chain.get_prompts()[0].pretty_print()

answer_prompt = ChatPromptTemplate.from_template(
    """Given the following user question, 
    corresponding SQL query, and SQL result, 
    answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

# First, generate and extract the SQL query
question = "Rank top 5 food in Thailand"
raw_response = write_query.invoke({"question": question})
sql_query = extract_sql(raw_response)

print("Generated SQL Query:")
print(sql_query)

# Now create a simpler chain that uses the extracted SQL
chain = (
    RunnablePassthrough.assign(
        result=lambda x: execute_query.invoke({"query": sql_query})
    )
    | answer_prompt
    | llm
    | StrOutputParser()
)

print("\nFinal Answer:")
print(chain.invoke({"question": question, "query": sql_query}))
