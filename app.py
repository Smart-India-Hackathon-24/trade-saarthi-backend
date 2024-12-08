from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from routes.RestrictedWordsRoutes import restricted_words_router
from routes.RestrictedPrefixSuffixRoutes import restricted_prefix_suffix_router
from config.RedisConfig import get_redis_client

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

@app.get("/test-redis", tags=["Health Check"])
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


# All Validate Title Routes
app.include_router(restricted_words_router)
app.include_router(restricted_prefix_suffix_router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
