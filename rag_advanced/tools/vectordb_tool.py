from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from config import embed_model
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# Global variable for vectorstore
_vectorstore = None

def _get_vectorstore():
    """Lazy load the vectorstore"""
    global _vectorstore
    if _vectorstore is None:
        # Get the correct path to eva.pdf
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(current_dir, "eva.pdf")
        
        # Load the PDF
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        split_docs = splitter.split_documents(docs)
        
        embeddings = OpenAIEmbeddings(model=embed_model)
        _vectorstore = Chroma.from_documents(split_docs, embeddings)
    
    return _vectorstore

def vectordb_search_tool(state):
    query = state["input"]
    vectorstore = _get_vectorstore()
    docs = vectorstore.similarity_search(query, k=3)
    return {"output": "\n\n".join([doc.page_content for doc in docs])}
