import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai_api_key = os.environ["OPENAI_API_KEY"]
model = os.environ["OPENAI_MODEL"]
embed_model = os.environ["OPENAI_EMBED_MODEL"]
temperature = os.environ["TEMPERATURE"]
tavily_api_key = os.environ["TAVILY_API_KEY"]

chunk_size = 1000
chunk_overlap = 150

pdf_policy_path = "/home/nam861836/ai-intern/rag_advanced/data/policy.pdf"
db_path = "/home/nam861836/ai-intern/rag_advanced/data/user_ticket.db"