import redis
import os
from config.base_config import BaseConfiguration
from typing import Optional

config = BaseConfiguration()
_redis_client: Optional[redis.Redis] = None

def redis_caching() -> Optional[redis.Redis]:
    """
    Get or create a singleton Redis client with connection pooling.
    This prevents creating multiple connections and improves performance.
    """
    global _redis_client
    
    if _redis_client is not None:
        try:
            # Quick health check
            _redis_client.ping()
            return _redis_client
        except (redis.ConnectionError, redis.TimeoutError):
            print("Redis connection lost, attempting to reconnect...")
            _redis_client = None
    
    try:
        # Create connection pool with proper settings
        pool = redis.ConnectionPool(
            host=config.redis_config.host,
            port=19002,
            password=config.redis_config.password.get_secret_value(),
            max_connections=500,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
            health_check_interval=30
        )
        
        _redis_client = redis.Redis(connection_pool=pool)
        
        # Test the connection
        _redis_client.ping()
        print("Redis connection established successfully with connection pooling")
        return _redis_client
        
    except redis.exceptions.ConnectionError as e:
        print(f"Redis connection failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error connecting to Redis: {e}")
        return None

