import os
from operator import itemgetter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, create_sql_query_chain,  create_retrieval_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools import QuerySQLDataBaseTool

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]
model = os.environ["OPENAI_MODEL"]
embed_model = os.environ["OPENAI_EMBED_MODEL"]
temperature = os.environ["TEMPERATURE"]

def load_and_split_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    split_docs = splitter.split_documents(docs)
    return split_docs

def create_retriever(documents):
    embeddings = OpenAIEmbeddings(model = embed_model)
    vectorstore = Chroma.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()
    return retriever



system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

llm = ChatOpenAI(model= model, temperature= temperature)

docs = load_and_split_pdf("../data/eva.pdf")
retriever = create_retriever(docs)

question_answer_chain = create_stuff_documents_chain(llm, prompt)

rag_chain = create_retrieval_chain(retriever, question_answer_chain)

print(type(rag_chain))

#results = rag_chain.invoke({"input": "What is faithfullness in RAGAS?"})
#print(results["answer"])

'''
create_stuff_documents_chain
The create_stuff_documents_chain takes a list of documents and formats them all into a prompt, then passes that prompt to an LLM. It passes ALL documents, so you should make sure it fits within the context window of the LLM you are using.

Taking a List of Documents: This function starts by receiving a group of documents that you provide.

Formatting into a Prompt: It then takes all these documents and organizes them into a specific prompt. A prompt is essentially a text setup that is used to feed information into a language model (like an LLM, or Large Language Model).

Passing to an LLM: After formatting the documents into a prompt, this function sends the formatted prompt to a language model. The model will process this information to perform tasks like answering questions, generating text, etc.

Fit within Context Window: The function sends all the documents at once to the LLM. However, it's important to make sure that the total length of the prompt does not exceed what the LLM can handle at one time. This limit is known as the "context window" of the LLM. If the prompt is too long, the model might not process it effectively.

In simpler terms, think of this chain as a way of taking several pieces of text, bundling them together in a specific way, and then feeding them to an LLM that reads and uses this bundled text to do its job. Just make sure the bundle isn’t too big for the LLM to handle at once!

create_retrieval_chain
The create_retrieval_chain takes in a user inquiry, which is then passed to the retriever to fetch relevant documents. Those documents (and original inputs) are then passed to an LLM to generate a response.

Receiving a User Inquiry: This process begins when a user asks a question or makes a request.

Using a Retriever to Fetch Documents: The function then uses a retriever to find documents that are relevant to the user's inquiry. This means it searches through available information to pick out parts that can help answer the question.

Passing Information to an LLM: After gathering the relevant documents, both these documents and the original user inquiry are sent to an LLM.

Generating a Response: The LLM processes all the information it receives to come up with an appropriate response, which is then given back to the user.

In simpler terms, this chain acts like a smart assistant that first looks up information based on your question, gathers useful details, and then uses those details along with your original question to craft a helpful answer.
'''
