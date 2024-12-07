from fastapi import APIRouter, Query
from functions.RestrictedListsFunctions import *


restricted_words_router = APIRouter(
    prefix="/restricted_words", tags=["Restricted Words"]
)


@restricted_words_router.get("/get")
async def restricted_words():
    return get_restricted_lists("words")


@restricted_words_router.post("/check")
async def check_restricted_words(
    title: str = Query(..., description="Title to check for restricted words")
):
    result = check_title_in_restricted_lists(title.lower(), "words")
    return {
        "status": "success",
        "input_title": title,
        "isValid": result["isValid"],
        "invalid_words": result["invalid_words"],
    }
