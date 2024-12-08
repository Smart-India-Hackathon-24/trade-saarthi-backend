from fastapi import APIRouter, Query
from functions.RestrictedListsFunctions import *
from functions.AddCacheToRedis import set_cache, get_cache

restricted_words_router = APIRouter(
    prefix="/restricted_words", tags=["Restricted Words"]
)


@restricted_words_router.get("/get")
async def restricted_words():
    try:
        cached_words = get_cache("restricted_words")
        if cached_words:
            return cached_words
        
        words = get_restricted_lists("words")
        set_cache("restricted_words", words)
        return words
    except Exception as e:
        return get_restricted_lists("words")


@restricted_words_router.post("/check")
async def check_restricted_words(
    title: str = Query(..., description="Title to check for restricted words")
):
    try:
        cache_key = f"restricted_words_check:{title.lower()}"
        cached_result = get_cache(cache_key)
        
        if cached_result:
            return cached_result
            
        result = check_title_in_restricted_lists(title.lower(), "words")
        response = {
            "status": "success",
            "input_title": title,
            "isValid": result["isValid"],
            "invalid_words": result["invalid_words"],
        }
        
        set_cache(cache_key, response, expiry_seconds=3600)  # Cache for 1 hour
        return response
    except Exception as e:
        result = check_title_in_restricted_lists(title.lower(), "words")
        return {
            "status": "success", 
            "input_title": title,
            "isValid": result["isValid"],
            "invalid_words": result["invalid_words"],
        }
