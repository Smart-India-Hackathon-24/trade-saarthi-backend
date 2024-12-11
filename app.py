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

from routes.RestrictedWordsRoutes import restricted_words_router,check_restricted_words
from routes.RestrictedPrefixSuffixRoutes import prefix_router, suffix_router, check_router,check_restricted_prefix_suffix
from routes.TitleCombinationRoute import title_combination_router,get_all_combinated_data,get_space_nospace_data
from routes.TradeMarkRoute import trademark_router
from models.TradeMarkModel import CommonResponse


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
        api_map={
            "Restricted Words":check_restricted_words,
            "Restricted Prefix/Suffix":check_restricted_prefix_suffix,
            "Title Combination":get_all_combinated_data,
            "Space No_Space":get_space_nospace_data,
            "Check Minimum Title Length":check_minimum_word
        }
        
        results={}
        for name,func in api_map.items():
            results[name]=await func(title_name)
        # result = api_map[api_name](data)
        # print(title_name,results)
        return {"status": "success","results":results},200
    
    except Exception as e:
        return {"status":"failed","message":f"Internal Server Error {e}"},500


@app.post("/check_min_word")
async def check_minimum_word(title:str):
    try:
        if not title:
            return CommonResponse(
                status="failed",
                input_title=title,
                isValid=False,
                invalid_words=[],
                Message="Title is required"
            ),400

        return CommonResponse(
                status="success",
                input_title=title,
                isValid=len(title.split())>1,
                invalid_words=[],
                Message=f"{title} has {len(title.split())} words"
            ),200
    except Exception as e:
        return CommonResponse(
                status="failed",
                input_title=title,
                isValid=False,
                invalid_words=[],
                Error=f"Internal Server Error {e}"
            ),500


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
