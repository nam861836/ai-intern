from config, prompts import *
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

def llm_model():
    llm = init_chat_model(OPENAI_MODEL, model_provider="openai")
    return llm

def generate_multi_query():
    multiquery_prompt_template = ChatPromptTemplate.from_template(multiquery_prompt)
