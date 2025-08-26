
import pytest
from unittest.mock import patch, MagicMock
from app.services.mongodb import get_mongo_client

@patch('app.services.mongodb.MongoClient')
@patch('app.services.mongodb.BaseConfiguration')
def test_get_mongo_client_success(mock_config, mock_mongo):
	# Mock config
	mock_config.return_value.mongodb_config.uri = 'mongodb://fakeuri'
	# Mock client and admin.command
	mock_client = MagicMock()
	mock_mongo.return_value = mock_client
	mock_client.admin.command.return_value = {'ok': 1}

	client = get_mongo_client()
	mock_client.admin.command.assert_called_once_with('ping')
	assert client is mock_client

@patch('app.services.mongodb.MongoClient')
@patch('app.services.mongodb.BaseConfiguration')
def test_get_mongo_client_failure(mock_config, mock_mongo):
	# Mock config
	mock_config.return_value.mongodb_config.uri = 'mongodb://fakeuri'
	# Mock client and admin.command
	mock_client = MagicMock()
	mock_mongo.return_value = mock_client
	mock_client.admin.command.side_effect = Exception('fail')

	client = get_mongo_client()
	mock_client.admin.command.assert_called_once_with('ping')
	assert client is None


