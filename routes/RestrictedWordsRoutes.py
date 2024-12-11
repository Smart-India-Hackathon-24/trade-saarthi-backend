from fastapi import APIRouter, Query
from functions.RestrictedListsFunctions import *
from functions.AddCacheToRedis import set_cache, get_cache
from functions.CsvOperations import CsvOperations
from utils.path_utils import get_data_file_path

restricted_words_router = APIRouter(
    prefix="/restricted_words", tags=["Restricted Words"]
)

WORDS_CSV_PATH = get_data_file_path("RestrictedWords.csv")

@restricted_words_router.get("/get")
async def restricted_words():
    try:
        cached_words = get_cache("restricted_words")
        if cached_words:
            return cached_words
        
        words = CsvOperations.read_csv(WORDS_CSV_PATH)
        set_cache("restricted_words", words)
        return words
    except Exception as e:
        return CsvOperations.read_csv(WORDS_CSV_PATH)

@restricted_words_router.post("/add")
async def add_restricted_word(word: str = Query(..., description="Word to add to restricted list")):
    result = CsvOperations.add_word(WORDS_CSV_PATH, word)
    if result["status"] == "success":
        # Clear cache to reflect new changes
        set_cache("restricted_words", CsvOperations.read_csv(WORDS_CSV_PATH))
    return result

@restricted_words_router.delete("/delete")
async def delete_restricted_word(word: str = Query(..., description="Word to delete from restricted list")):
    result = CsvOperations.delete_word(WORDS_CSV_PATH, word)
    if result["status"] == "success":
        # Clear cache to reflect new changes
        set_cache("restricted_words", CsvOperations.read_csv(WORDS_CSV_PATH))
    return result

@restricted_words_router.post("/check")
async def check_restricted_words(
    title: str = Query(..., description="Title to check for restricted words")
):
    try:
        cache_key = f"restricted_words_check:{title.lower()}"
        cached_result = get_cache(cache_key)
        
        if cached_result:
            return cached_result
            
        words = CsvOperations.read_csv(WORDS_CSV_PATH)
        title_words = title.lower().split()
        invalid_words = [word for word in title_words if word in words]
        
        response = {
            "status": "success",
            "input_title": title,
            "isValid": len(invalid_words) == 0,
            "invalid_words": invalid_words,
        }
        
        set_cache(cache_key, response, expiry_seconds=3600)  # Cache for 1 hour
        return response
    except Exception as e:
        return {"status": "error", "message": str(e)}
