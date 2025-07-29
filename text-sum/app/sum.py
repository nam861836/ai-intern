import os
from operator import itemgetter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langchain_community.document_loaders import WebBaseLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]
model = os.environ["OPENAI_MODEL"]
embed_model = os.environ["OPENAI_EMBED_MODEL"]
temperature = os.environ["TEMPERATURE"]
os.environ['USER_AGENT'] = 'myagent'

loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
docs = loader.load()

#print(docs)

llm = ChatOpenAI(model= model, temperature= temperature)

prompt = ChatPromptTemplate.from_messages(
    [("system", "Write a concise summary of the following:\\n\\n{context}")]
)

# Instantiate chain
chain = create_stuff_documents_chain(llm, prompt)

# Invoke chain
result = chain.invoke({"context": docs})

#for token in chain.stream({"context": docs}):
#    print(token, end="|")