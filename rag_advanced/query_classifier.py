from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import model, temperature
from langchain.chat_models import init_chat_model

prompt = PromptTemplate.from_template(
"""
You are a classification agent that determines how to route a user query to the appropriate system. Your job is to **only return one of the following labels** based on the query's content:

- "sql" → if the question is about account details, billing, or support tickets
- "tavily" → if the question is a general or technical query (e.g., troubleshooting, how-to, product comparisons, etc.)
- "vectordb" → if the question refers to internal company policies, employee handbooks, or document content

Use the following process:
1. Read the user query.
2. Identify the main topic or intent.
3. Match it to the most appropriate category.
4. Respond with only the label: "sql", "tavily", or "vectordb".

Now classify this query:

Query: {query}
Answer:
"""
)
def llm_model():
    llm = init_chat_model(model, model_provider="openai", temperature=temperature)
    return llm

def classify_query(query: str) -> str:
    llm = llm_model()
    response = llm.invoke(prompt.format(query=query))
    return response.content.strip().lower()
