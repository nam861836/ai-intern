import warnings
warnings.filterwarnings("ignore")

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
from langchain.load import dumps, loads



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
    "don't know. Use five sentences maximum and keep the "
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

template = """You are an AI language model assistant. Your task is to generate five 
different versions of the given user question to retrieve relevant documents from a vector 
database. By generating multiple perspectives on the user question, your goal is to help
the user overcome some of the limitations of the distance-based similarity search. 
Provide these alternative questions separated by newlines. Original question: {question}"""
prompt_perspectives = ChatPromptTemplate.from_template(template)

llm = ChatOpenAI(model= model, temperature= temperature)

docs = load_and_split_pdf("../data/eva.pdf")
vectorstore = create_vectorstore(docs)

bm25 = BM25Retriever.from_documents(docs)
dense = vectorstore.as_retriever()

hybrid = EnsembleRetriever(retrievers=[dense, bm25], weights=[0.7, 0.3])

reranker = CrossEncoder('cross-encoder/ms-marco-TinyBERT-L2-v2')

generate_queries = (
    prompt_perspectives 
    | llm
    | StrOutputParser() 
    | (lambda x: x.split("\n"))
)

# --- Retrieval + Rerank logic ---
def multi_query_retrieve_and_rerank(inputs: dict):
    question = inputs["input"]
    
    # Step 1: Generate multiple queries
    sub_queries = generate_queries.invoke({"question": question})
    print(sub_queries)
    
    # Step 2: Retrieve docs for each sub-query
    all_docs = []
    for q in sub_queries:
        docs = hybrid.get_relevant_documents(q)
        all_docs.extend(docs)
    
    # Step 3: Remove duplicates
    flattened = list(set(dumps(doc) for doc in all_docs))
    unique_docs = [loads(doc) for doc in flattened]
    
    # Step 4: Rerank with original question
    pairs = [(question, doc.page_content) for doc in unique_docs]
    scores = reranker.predict(pairs)
    
    # Step 5: Sort and select top 4
    reranked = sorted(zip(unique_docs, scores), key=lambda x: x[1], reverse=True)
    top_docs = [doc for doc, _ in reranked[:10]]
    context = "\n\n".join([doc.page_content for doc in top_docs])
    
    return {"input": question, "context": context}

retrieval_chain = RunnableLambda(multi_query_retrieve_and_rerank)

# Final chain
final_chain = retrieval_chain | prompt | llm | StrOutputParser()

# Run
response = final_chain.invoke({"input": "What are the strategies to evaluate a RAG system?"})
print(response)

