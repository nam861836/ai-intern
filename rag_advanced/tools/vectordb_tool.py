from langchain_community.vectorstores import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever    
from langchain_openai import OpenAIEmbeddings
import config
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from typing import List
from langchain_core.output_parsers import BaseOutputParser
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
import config
from langchain.chains.combine_documents import create_stuff_documents_chain
from prompts import POLICY_PROMPT

llm = ChatOpenAI(model=config.model, temperature=config.temperature)

def load_and_split_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=config.chunk_size, chunk_overlap=config.chunk_overlap)
    split_docs = splitter.split_documents(docs)
    
    return split_docs

def create_vectorstore(documents):
    embeddings = OpenAIEmbeddings(model = config.embed_model)
    vectorstore = Chroma.from_documents(documents, embeddings)
    return vectorstore

def ensemble(docs, vectorstore, query):
    bm25 = BM25Retriever.from_documents(docs)
    multiquery_retriever = MultiQueryRetriever.from_llm(
        retriever=vectorstore.as_retriever(),
        llm = llm
    )
    ensemble_retriever = EnsembleRetriever(
        retrievers=[multiquery_retriever, bm25],
        weights=[0.5, 0.5]
    )
    ensemble_docs = ensemble_retriever.invoke(query)
    print(ensemble_docs)
    return ensemble_docs

def RAG(state):
    query = state["input"]
    split_docs = load_and_split_pdf(config.pdf_policy_path)
    vectorstore = create_vectorstore(split_docs)

    context = ensemble(split_docs, vectorstore, query)
    print("1")
    prompt = ChatPromptTemplate.from_template(POLICY_PROMPT)
    print("2")
    qa_chain = create_stuff_documents_chain(llm, prompt)
    print("3")
    rag_response = qa_chain.invoke({
        "input": query,
        "context": context
    })
    print("4")
    print(type(rag_response))
    return {"input": query, "output": rag_response}
