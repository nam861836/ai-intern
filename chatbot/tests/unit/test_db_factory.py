from unittest.mock import patch, MagicMock
from app.factories.db_factory import DBFactory

@patch('app.factories.db_factory.SQLDatabase')
def test_create_db(mock_sql_db):
    DBFactory.create_db()
    mock_sql_db.from_uri.assert_called()

@patch('app.factories.db_factory.create_sql_agent')
@patch('app.factories.db_factory.LLMFactory.create')
@patch('app.factories.db_factory.DBFactory.create_db')
@patch('app.factories.db_factory.SQLDatabaseToolkit')
def test_create_sql_agent(mock_toolkit, mock_create_db, mock_llm, mock_create_sql_agent):
    mock_db = MagicMock()
    mock_create_db.return_value = mock_db
    mock_llm.return_value = MagicMock()
    mock_toolkit.return_value = MagicMock()
    DBFactory.create_sql_agent()
    mock_create_sql_agent.assert_called()
