from fastapi import APIRouter, Query
from functions.RestrictedListsFunctions import *
from config.RedisConfig import get_redis_client

restricted_words_router = APIRouter(
    prefix="/restricted_words", tags=["Restricted Words"]
)


@restricted_words_router.get("/get")
async def restricted_words():
    try:
        redis_client = get_redis_client()
        cached_words = redis_client.get("restricted_words")
        if cached_words:
            return cached_words
        
        words = get_restricted_lists("words")
        redis_client.set("restricted_words", words)
        return words
    except Exception as e:
        return get_restricted_lists("words")


@restricted_words_router.post("/check")
async def check_restricted_words(
    title: str = Query(..., description="Title to check for restricted words")
):
    try:
        redis_client = get_redis_client()
        cache_key = f"restricted_words_check:{title.lower()}"
        cached_result = redis_client.get(cache_key)
        
        if cached_result:
            return cached_result
            
        result = check_title_in_restricted_lists(title.lower(), "words")
        response = {
            "status": "success",
            "input_title": title,
            "isValid": result["isValid"],
            "invalid_words": result["invalid_words"],
        }
        
        redis_client.set(cache_key, response, ex=3600)  # Cache for 1 hour
        return response
    except Exception as e:
        result = check_title_in_restricted_lists(title.lower(), "words")
        return {
            "status": "success", 
            "input_title": title,
            "isValid": result["isValid"],
            "invalid_words": result["invalid_words"],
        }
