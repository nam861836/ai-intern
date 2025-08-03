from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import model, temperature

prompt = PromptTemplate.from_template(
"""
You are a router that classifies queries:
- If it's about account info or tickets → respond with "sql"
- If it's about tech questions → respond with "tavily"
- If it's about company policies or documents → respond with "vectordb"

Query: {query}
Answer:
""")

llm = ChatOpenAI(model=model, temperature=temperature)

def classify_query(query: str) -> str:
    response = llm.invoke(prompt.format(query=query))
    # Extract the content from the AIMessage
    return response.content.strip().lower()
