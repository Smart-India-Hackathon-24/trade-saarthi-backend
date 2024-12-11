from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from pymilvus import connections
import json
from config.database import connect_db
from config.RedisConfig import get_redis_client
from routes.RedisRoutes import redis_router
import re

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
async def unified_endpoint(title:str):
    try:
        api_map={
            "Restricted Words":check_restricted_words,
            "Restricted Prefix/Suffix":check_restricted_prefix_suffix,
            "Title Combination":get_all_combinated_data,
            "Space No_Space":get_space_nospace_data,
            "Check Minimum Title Length":check_minimum_word,
            "Check Special Characters":check_special_character
        }
        
        results={}
        for name,func in api_map.items():
            results[name]=await func(title)
        print(results)

        def extract_is_valid(response):
            if isinstance(response, CommonResponse):
                return response.isValid
            elif isinstance(response, dict):
                return response.get("isValid", None)
            elif isinstance(response, tuple) and isinstance(response[0], CommonResponse):
                return response[0].isValid
            return None

        # result_str = f"""function(
        #     "{title}", 
        #     {extract_is_valid(results["Restricted Words"])}, # Restricted Words
        #     {extract_is_valid(results["Restricted Prefix/Suffix"])}, # Restricted Prefix/Suffix
        #     {extract_is_valid(results["Title Combination"])}, # Title Combination
        #     {extract_is_valid(results["Space No_Space"])}, # Space No_Space
        #     {extract_is_valid(results["Check Minimum Title Length"])} # Check Minimum Title Length
        # );"""
        # Generate the output lines
        output_lines = []
        d={}
        for key, response in results.items():
            is_valid = extract_is_valid(response)
            d[key.upper()] = is_valid
            # output_lines.append(f"{key.upper()} : {str(is_valid).upper()}")
        
        # Combine the lines into a single output string
        output_string = "\n".join(output_lines)

        return {"status": "success","results":results,"final_output":d}
    
    except Exception as e:
        return {"status":"failed","message":f"Internal Server Error {e}"}


@app.post("/check_min_word")
async def check_minimum_word(title:str):
    try:
        if not title:
            return CommonResponse(
                status="failed",
                input_title=title,
                isValid=False,
                invalid_words=[],
                message="Title is required"
            )

        return CommonResponse(
                status="success",
                input_title=title,
                isValid=len(title.split())>1,
                invalid_words=[],
                message=f"{title} has {len(title.split())} words"
            )
    except Exception as e:
        return CommonResponse(
                status="failed",
                input_title=title,
                isValid=False,
                invalid_words=[],
                error=f"Internal Server Error {e}"
            )


def contains_special_characters(string: str) -> bool:
    # Define special characters regex
    pattern = r"[*.#@!$%^&*(),?\":{}|<>]"
    return bool(re.search(pattern, string))


@app.post("/check_spec_char")
async def check_special_character(title:str):
    try:
        pattern = r"[*.#@!$%^&*(),?\":{}|<>]"
        if not title:
            return CommonResponse(
                status="failed",
                input_title=title,
                isValid=False,
                invalid_words=[],
                message="Title is required"
            )
        print(re.search(pattern,title))
        if bool(re.search(pattern,title)):
            return CommonResponse(
                status="success",
                input_title=title,
                isValid=False,
                invalid_words=[],
                message=f"{title} has special characters which are not allowed "
            )
        return CommonResponse(
                status="success",
                input_title=title,
                isValid=True,
                invalid_words=[],
                message=f"{title} is allowed "
            )
    
    except Exception as e:
        return CommonResponse(
                    status="failed",
                    input_title=title,
                    isValid=False,
                    invalid_words=[],
                    error=f"Internal Server Error {e}"
                )

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
