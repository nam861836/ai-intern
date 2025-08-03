import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai_api_key = os.environ["OPENAI_API_KEY"]
model = os.environ["OPENAI_MODEL"]
embed_model = os.environ["OPENAI_EMBED_MODEL"]
temperature = os.environ["TEMPERATURE"]
tavily_api_key = os.environ["TAVILY_API_KEY"]