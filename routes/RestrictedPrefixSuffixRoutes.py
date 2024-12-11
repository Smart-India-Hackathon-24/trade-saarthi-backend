from fastapi import APIRouter, Query
from functions.RestrictedListsFunctions import *
from functions.AddCacheToRedis import set_cache, get_cache
from functions.CsvOperations import CsvOperations
from utils.path_utils import get_data_file_path

restricted_prefix_suffix_router = APIRouter(
    prefix="/restricted_prefix_suffix", tags=["Restricted Prefix Suffix"]
)

PREFIX_CSV_PATH = get_data_file_path("RestrictedPrefix.csv")
SUFFIX_CSV_PATH = get_data_file_path("RestrictedSuffix.csv")

@restricted_prefix_suffix_router.get("/get_prefix")
async def get_restricted_prefix():
    try:
        cached_words = get_cache("restricted_prefix")
        if cached_words:
            return cached_words
        
        words = CsvOperations.read_csv(PREFIX_CSV_PATH)
        set_cache("restricted_prefix", words)
        return words
    except Exception as e:
        return CsvOperations.read_csv(PREFIX_CSV_PATH)

@restricted_prefix_suffix_router.get("/get_suffix")
async def get_restricted_suffix():
    try:
        cached_words = get_cache("restricted_suffix")
        if cached_words:
            return cached_words
        
        words = CsvOperations.read_csv(SUFFIX_CSV_PATH)
        set_cache("restricted_suffix", words)
        return words
    except Exception as e:
        return CsvOperations.read_csv(SUFFIX_CSV_PATH)

@restricted_prefix_suffix_router.post("/add_prefix")
async def add_restricted_prefix(prefix: str = Query(..., description="Prefix to add to restricted list")):
    result = CsvOperations.add_word(PREFIX_CSV_PATH, prefix)
    if result["status"] == "success":
        set_cache("restricted_prefix", CsvOperations.read_csv(PREFIX_CSV_PATH))
    return result

@restricted_prefix_suffix_router.post("/add_suffix")
async def add_restricted_suffix(suffix: str = Query(..., description="Suffix to add to restricted list")):
    result = CsvOperations.add_word(SUFFIX_CSV_PATH, suffix)
    if result["status"] == "success":
        set_cache("restricted_suffix", CsvOperations.read_csv(SUFFIX_CSV_PATH))
    return result

@restricted_prefix_suffix_router.delete("/delete_prefix")
async def delete_restricted_prefix(prefix: str = Query(..., description="Prefix to delete from restricted list")):
    result = CsvOperations.delete_word(PREFIX_CSV_PATH, prefix)
    if result["status"] == "success":
        set_cache("restricted_prefix", CsvOperations.read_csv(PREFIX_CSV_PATH))
    return result

@restricted_prefix_suffix_router.delete("/delete_suffix")
async def delete_restricted_suffix(suffix: str = Query(..., description="Suffix to delete from restricted list")):
    result = CsvOperations.delete_word(SUFFIX_CSV_PATH, suffix)
    if result["status"] == "success":
        set_cache("restricted_suffix", CsvOperations.read_csv(SUFFIX_CSV_PATH))
    return result

@restricted_prefix_suffix_router.post("/check")
async def check_restricted_prefix_suffix(
    title: str = Query(..., description="Title to check for restricted prefix and suffix")
):
    try:
        cache_key = f"restricted_prefix_suffix_check:{title.lower()}"
        cached_result = get_cache(cache_key)
        
        if cached_result:
            return cached_result
        
        title = title.lower().strip()
        prefixes = CsvOperations.read_csv(PREFIX_CSV_PATH)
        suffixes = CsvOperations.read_csv(SUFFIX_CSV_PATH)
        
        invalid_words = []
        
        # Check if title starts with any restricted prefix
        for prefix in prefixes:
            if title.startswith(prefix):
                invalid_words.append(f"prefix:{prefix}")
                
        # Check if title ends with any restricted suffix
        for suffix in suffixes:
            if title.endswith(suffix):
                invalid_words.append(f"suffix:{suffix}")
        
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
