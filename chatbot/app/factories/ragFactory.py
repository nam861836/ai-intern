from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from factories.llmFactory import LLMFactory
from config.base_config import BaseConfiguration
from utils.prompts import POLICY_PROMPT

config = BaseConfiguration()

class RAGFactory:
    @staticmethod
    def load_and_split_pdf(file_path: str):
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap
        )
        return splitter.split_documents(docs)

    @staticmethod
    def create_vectorstore(documents):
        embeddings = OpenAIEmbeddings(
            model=config.embedding_model_config.embed_model,
            api_key=config.embedding_model_config.api_key.get_secret_value()
        )
        return Chroma.from_documents(documents, embeddings)

    @staticmethod
    def create_ensemble_retriever(docs, vectorstore):
        llm = LLMFactory.create()
        bm25 = BM25Retriever.from_documents(docs)
        multiquery_retriever = MultiQueryRetriever.from_llm(
            retriever=vectorstore.as_retriever(),
            llm=llm
        )
        return EnsembleRetriever(
            retrievers=[multiquery_retriever, bm25],
            weights=[0.5, 0.5]
        )

    @staticmethod
    def create_rag_chain():
        llm = LLMFactory.create()
        prompt = ChatPromptTemplate.from_template(POLICY_PROMPT)
        return create_stuff_documents_chain(llm, prompt)
