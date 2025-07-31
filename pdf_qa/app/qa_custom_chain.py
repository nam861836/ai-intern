import os
from operator import itemgetter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser


from sentence_transformers import CrossEncoder
from langchain_core.documents import Document

from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

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

def create_vectorstore(documents):
    embeddings = OpenAIEmbeddings(model = embed_model)
    vectorstore = Chroma.from_documents(documents, embeddings)
    return vectorstore



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
vectorstore = create_vectorstore(docs)

bm25 = BM25Retriever.from_documents(docs)
dense = vectorstore.as_retriever()

hybrid = EnsembleRetriever(retrievers=[dense, bm25], weights=[0.5, 0.5])

def retrieve_context(inputs: dict):
    query = inputs["input"]
    retrieved_docs = hybrid.get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    return {"input": query, "context": context}

retrieval_chain = RunnableLambda(retrieve_context)

chain = retrieval_chain | prompt | llm | StrOutputParser()

query = "What are the strategies to evaluate a RAG system?"
response = chain.invoke({"input": query})
print(response)