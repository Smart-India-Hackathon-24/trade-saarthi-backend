from fastapi import APIRouter, Query
from functions.RestrictedListsFunctions import *

title_combination_router = APIRouter(
    prefix="/title_combination", tags=["Title Combination"]
)

