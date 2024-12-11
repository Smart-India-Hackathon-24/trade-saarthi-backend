from fastapi import APIRouter
from config.RedisConfig import get_redis_client
import json

redis_router = APIRouter(
    prefix="/redis",
    tags=["Redis APIs"]
)

@redis_router.get("/test")
async def test_redis():
    try:
        redis_client = get_redis_client()
        redis_client.set("test", "Hello Redis!")
        value = redis_client.get("test")
        return {
            "status": "success",
            "message": "Redis is working!",
            "test_value": value,
        }
    except Exception as e:
        return {"status": "error", "message": f"Redis error: {str(e)}"}

@redis_router.get("/status")
async def get_cache_status():
    try:
        redis_client = get_redis_client()
        # Get all keys
        all_keys = redis_client.keys("*")

        cache_data = {}
        for key in all_keys:
            value = redis_client.get(key)
            # Try to decode JSON values
            try:
                decoded_value = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                decoded_value = value.decode('utf-8') if isinstance(value, bytes) else value
                
            # Get TTL for each key
            ttl = redis_client.ttl(key)
            cache_data[key] = {"value": decoded_value, "ttl_seconds": ttl}

        return {
            "status": "success",
            "cached_items_count": len(all_keys),
            "cached_data": cache_data,
        }
    except Exception as e:
        return {"status": "error", "message": f"Error fetching cache data: {str(e)}"}

@redis_router.delete("/clear/{cache_name}")
async def delete_cache_by_name(cache_name: str):
    try:
        redis_client = get_redis_client()
        if redis_client.exists(cache_name):
            redis_client.delete(cache_name)
            return {
                "status": "success",
                "message": f"Cache '{cache_name}' deleted successfully"
            }
        return {
            "status": "error",
            "message": f"Cache '{cache_name}' not found"
        }
    except Exception as e:
        return {"status": "error", "message": f"Error deleting cache: {str(e)}"}

@redis_router.delete("/clear-all")
async def delete_all_cache():
    try:
        redis_client = get_redis_client()
        keys_count = len(redis_client.keys("*"))
        redis_client.flushall()
        return {
            "status": "success",
            "message": f"All cache cleared successfully. {keys_count} keys were deleted."
        }
    except Exception as e:
        return {"status": "error", "message": f"Error clearing cache: {str(e)}"} 