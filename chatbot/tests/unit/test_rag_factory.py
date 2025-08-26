from unittest.mock import patch, MagicMock
from app.factories.rag_factory import RAGFactory

@patch('app.factories.rag_factory.PyPDFLoader')
@patch('app.factories.rag_factory.RecursiveCharacterTextSplitter')
def test_load_and_split_pdf(mock_splitter, mock_loader):
    mock_loader.return_value.load.return_value = ['doc']
    mock_splitter.return_value.split_documents.return_value = ['chunk']
    chunks = RAGFactory.load_and_split_pdf('file.pdf')
    assert chunks == ['chunk']

@patch('app.factories.rag_factory.OpenAIEmbeddings')
@patch('app.factories.rag_factory.Chroma')
def test_create_vectorstore(mock_chroma, mock_embeddings):
    mock_embeddings.return_value = MagicMock()
    mock_chroma.from_documents.return_value = 'vectorstore'
    result = RAGFactory.create_vectorstore(['doc'])
    assert result == 'vectorstore'

@patch('app.factories.rag_factory.LLMFactory.create')
@patch('app.factories.rag_factory.BM25Retriever')
@patch('app.factories.rag_factory.MultiQueryRetriever')
@patch('app.factories.rag_factory.EnsembleRetriever')
def test_create_ensemble_retriever(mock_ensemble, mock_multi, mock_bm25, mock_llm):
    mock_bm25.from_documents.return_value = 'bm25'
    mock_multi.from_llm.return_value = 'multiquery'
    mock_ensemble.return_value = 'ensemble'
    result = RAGFactory.create_ensemble_retriever(['doc'], MagicMock())
    assert result == 'ensemble'

@patch('app.factories.rag_factory.LLMFactory.create')
@patch('app.factories.rag_factory.ChatPromptTemplate')
@patch('app.factories.rag_factory.create_stuff_documents_chain')
def test_create_rag_chain(mock_chain, mock_prompt, mock_llm):
    mock_llm.return_value = MagicMock()
    mock_prompt.from_template.return_value = 'prompt'
    mock_chain.return_value = 'chain'
    result = RAGFactory.create_rag_chain()
    assert result == 'chain'
