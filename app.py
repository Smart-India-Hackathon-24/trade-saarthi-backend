from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from pymilvus import connections
import json
from config.database import connect_db
from config.RedisConfig import get_redis_client
from routes.RedisRoutes import redis_router


# Connect to Zilliz Cloud
connections.connect(
    alias="default",
    uri=os.getenv("ZILLIZ_URI"),
    token=os.getenv("ZILLIZ_TOKEN")    
)

connect_db()

from routes.RestrictedWordsRoutes import restricted_words_router
from routes.RestrictedPrefixSuffixRoutes import prefix_router, suffix_router, check_router
from routes.TitleCombinationRoute import title_combination_router
from routes.TradeMarkRoute import trademark_router



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


@app.post("/unified_endpoint")
async def unified_endpoint(title_name:str):
    try:
        # api_name = payload.get("api_name")
        # data = payload.get("data", {})
        
        # if not api_name or api_name not in api_map:
        #     raise HTTPException(status_code=400, detail="Invalid or missing API name.")
        api_map={
            ""
        }
        # # Call the corresponding API function
        # result = api_map[api_name](data)
        print(title_name)
        result=""
        return {"status": "success", "result": result}
    
    except Exception as e:
        return {"status":"failed","message":f"Internal Server Error {e}"},500

# All Validate Title Routes
app.include_router(restricted_words_router)
app.include_router(prefix_router)
app.include_router(suffix_router)
app.include_router(check_router)
app.include_router(title_combination_router)
app.include_router(trademark_router)
app.include_router(redis_router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
