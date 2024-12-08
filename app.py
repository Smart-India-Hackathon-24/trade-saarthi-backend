from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from routes.RestrictedWordsRoutes import restricted_words_router
from routes.RestrictedPrefixSuffixRoutes import restricted_prefix_suffix_router
from config.RedisConfig import get_redis_client
import json

app = FastAPI(
    title="Trade Mark Sarthi", description="apis for new paper ", version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health Check"])
async def root():
    return {"status": "success", "message": "Server is running!"}


@app.get("/test-redis", tags=["Redis APIs"])
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


@app.get("/cache-status", tags=["Redis APIs"])
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


# All Validate Title Routes
app.include_router(restricted_words_router)
app.include_router(restricted_prefix_suffix_router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
