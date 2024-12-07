from fastapi import APIRouter, Query
from functions.RestrictedListsFunctions import *


restricted_prefix_suffix_router = APIRouter(
    prefix="/restricted_prefix_suffix", tags=["Restricted Prefix Suffix"]
)


@restricted_prefix_suffix_router.get("/get")
async def restricted_prefix_suffix():
    return get_restricted_lists("prefix_suffix")


@restricted_prefix_suffix_router.post("/check")
async def check_restricted_prefix_suffix(
    title: str = Query(..., description="Title to check for restricted prefix suffix")
):
    result = check_title_in_restricted_lists(title.lower(), "prefix_suffix")
    return {
        "status": "success",
        "input_title": title,
        "isValid": result["isValid"],
        "invalid_words": result["invalid_words"],
    }
