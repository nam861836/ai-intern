from unittest.mock import patch, MagicMock
import pytest
from tools import db_query_tool, rag_tool, tavily_search_tool

def test_db_query():
    with patch('tools.db_query_tool.DBFactory.create_sql_agent') as mock_agent:
        mock_agent.return_value.invoke.return_value = 'result'
        assert db_query_tool.db_query.invoke('query') == 'result'

def test_rag():
    with patch('tools.rag_tool.RAGFactory.load_and_split_pdf') as mock_split, \
         patch('tools.rag_tool.RAGFactory.create_vectorstore') as mock_vector, \
         patch('tools.rag_tool.RAGFactory.create_ensemble_retriever') as mock_retriever, \
         patch('tools.rag_tool.RAGFactory.create_rag_chain') as mock_chain:
        mock_split.return_value = ['doc']
        mock_vector.return_value = MagicMock()
        mock_retriever.return_value = MagicMock()
        mock_chain.return_value.invoke.return_value = 'rag_result'
        assert rag_tool.RAG.invoke('query') == 'rag_result'

def test_tavily_search_tool():
    with patch('tools.tavily_search_tool.SearchFactory.get_tavily') as mock_tavily:
        mock_tavily.return_value.invoke.return_value = 'search_result'
        assert tavily_search_tool.tavily_search_tool.invoke('query') == 'search_result'
