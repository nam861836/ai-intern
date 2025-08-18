from factories.rag_factory import RAGFactory
from config.base_config import BaseConfiguration
from langchain.tools import tool
#from config import configs
config = BaseConfiguration()

@tool
def RAG(query: str) -> str:
    """
    Tool to create a simple RAG pipeline
    """

    pdf_policy_path = "/home/nam861836/Documents/ai-intern/chatbot/data/policy.pdf"
    split_docs = RAGFactory.load_and_split_pdf(pdf_policy_path)
    vectorstore = RAGFactory.create_vectorstore(split_docs)
    retriever = RAGFactory.create_ensemble_retriever(split_docs, vectorstore)
    context = retriever.invoke(query)
    chain = RAGFactory.create_rag_chain()
    return str(chain.invoke({"input": query, "context": context}))

