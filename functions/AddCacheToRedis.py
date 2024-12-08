from config.RedisConfig import get_redis_client
import json
from typing import Any, Optional

def set_cache(key: str, value: Any, expiry_seconds: Optional[int] = None) -> bool:
    """
    Set a value in Redis cache with optional expiry
    
    Args:
        key: Redis key
        value: Value to cache (will be JSON serialized)
        expiry_seconds: Optional TTL in seconds
        
    Returns:
        bool: True if successful, False if failed
    """
    try:
        redis_client = get_redis_client()
        serialized_value = json.dumps(value)
        if expiry_seconds:
            redis_client.set(key, serialized_value, ex=expiry_seconds)
        else:
            redis_client.set(key, serialized_value)
        return True
    except Exception as e:
        print(f"Error setting cache: {str(e)}")
        return False

def get_cache(key: str) -> Optional[Any]:
    """
    Get a value from Redis cache
    
    Args:
        key: Redis key
        
    Returns:
        Any: Deserialized value if found, None if not found or error
    """
    try:
        redis_client = get_redis_client()
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"Error getting cache: {str(e)}")
        return None 