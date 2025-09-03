import pytest
from unittest.mock import patch, MagicMock
from services import redis_caching

@patch('services.redis_caching.redis.Redis')
def test_redis_caching_reconnect_on_error(mock_redis):
    mock_client = MagicMock()
    mock_client.ping.side_effect = [redis_caching.redis.ConnectionError, None]
    mock_redis.return_value = mock_client
    redis_caching._redis_client = mock_client
    client = redis_caching.redis_caching()
    assert client is not None

@patch('services.redis_caching.redis.Redis')
def test_redis_caching_connection_failure(mock_redis):
    mock_redis.side_effect = redis_caching.redis.ConnectionError
    redis_caching._redis_client = None
    client = redis_caching.redis_caching()
    assert client is None
