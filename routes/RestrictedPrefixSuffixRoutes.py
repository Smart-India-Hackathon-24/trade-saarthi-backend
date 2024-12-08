from fastapi import APIRouter, Query
from functions.RestrictedListsFunctions import *
from config.RedisConfig import get_redis_client


restricted_prefix_suffix_router = APIRouter(
    prefix="/restricted_prefix_suffix", tags=["Restricted Prefix Suffix"]
)


@restricted_prefix_suffix_router.get("/get")
async def restricted_prefix_suffix():
    try:
        redis_client = get_redis_client()
        cached_words = redis_client.get("restricted_prefix_suffix")
        if cached_words:
            return cached_words
        
        words = get_restricted_lists("prefix_suffix")
        redis_client.set("restricted_prefix_suffix", words)
        return words
    except Exception as e:
        return get_restricted_lists("prefix_suffix")


@restricted_prefix_suffix_router.post("/check")
async def check_restricted_prefix_suffix(
    title: str = Query(..., description="Title to check for restricted prefix suffix")
):
    try:
        redis_client = get_redis_client()
        cache_key = f"restricted_prefix_suffix_check:{title.lower()}"
        cached_result = redis_client.get(cache_key)
        
        if cached_result:
            return cached_result
            
        result = check_title_in_restricted_lists(title.lower(), "prefix_suffix")
        response = {
            "status": "success",
            "input_title": title,
            "isValid": result["isValid"],
            "invalid_words": result["invalid_words"],
        }
        
        redis_client.set(cache_key, response, ex=3600)  # Cache for 1 hour
        return response
    except Exception as e:
        result = check_title_in_restricted_lists(title.lower(), "prefix_suffix")
        return {
            "status": "success",
            "input_title": title,
            "isValid": result["isValid"],
            "invalid_words": result["invalid_words"],
        }
