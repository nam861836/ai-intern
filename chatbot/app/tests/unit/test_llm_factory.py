from unittest.mock import patch, MagicMock
from factories.llm_factory import LLMFactory

@patch('factories.llm_factory.ChatOpenAI')
@patch('factories.llm_factory.config')
def test_llm_factory_create(mock_config, mock_chat_openai):
    mock_config.chat_model_config.model = 'gpt-3.5'
    mock_config.chat_model_config.temperature = 0.1
    mock_chat_openai.return_value = MagicMock()
    llm = LLMFactory.create()
    mock_chat_openai.assert_called_with(model='gpt-3.5', temperature=0.1)
