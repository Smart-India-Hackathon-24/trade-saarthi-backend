from fastapi import APIRouter, Query
from functions.RestrictedListsFunctions import *
from models.TradeMarkModel import CommonResponse
from config.database import get_collection
title_combination_router = APIRouter(
    prefix="/title_combination", tags=["Title Combination"]
)


def read_column_from_db(column_name='Title_Name'):
    column_values = []

    try:
        collection=get_collection("Alphabetic_sort_2")

        iterator = collection.query_iterator(
        expr="",output_fields=["Title_Name"])
        
        results = []
        columns=[]
        while True:
            result=iterator.next()
            if not result:
                iterator.close()
                break
            for record in result:
                column_values.append(record.get("Title_Name"))
            results+=result
        return column_values
    except FileNotFoundError:
        return []

# Initialize with empty list if file not found
# COLUMN_VALUE = read_column_from_csv()
COLUMN_VALUE = read_column_from_db()

@title_combination_router.get("/")
async def get_all_combinated_data(title: str = Query(..., description="The name to search for")):
    try:
        name=title.upper()
        def load_word_list(words_list):
            return set(words_list)

        def is_word_combination(input_string, word_set):
            words = input_string.split()
            
            def can_split(start, memo=None):
                if memo is None:
                    memo = {}
                
                if start == len(words):
                    return True
                
                if start in memo:
                    return memo[start]
                
                for end in range(start + 1, len(words) + 1):
                    current_phrase = ' '.join(words[start:end])
                    
                    if current_phrase in word_set:
                        if can_split(end, memo):
                            memo[start] = True
                            return True
                
                memo[start] = False
                return False
            
            return can_split(0)

        def test_word_combination_checker():
            title_names = COLUMN_VALUE
            word_set = load_word_list(title_names)
            

            name_validation = is_word_combination(name, word_set)

            return name_validation

        name_validation = test_word_combination_checker()

        if name_validation:
            return CommonResponse(
                status="success",
                input_title=name,
                isValid=False,
                invalid_words=[],
                message=f"{name} is combination of titles !",
            )
        else:
            return CommonResponse(
                status="success",
                input_title=name,
                isValid=True,
                invalid_words=[],
                message=f"{name} is not a combination of titles !"
            )
    except Exception as e:
        return CommonResponse(
                status="failed",
                input_title=name,
                isValid=False,
                invalid_words=[],
                error=f"Internal Server Error {e}"
            )


@title_combination_router.get("/space_nospace")
async def get_space_nospace_data(title: str = Query(..., description="The name to search for")):
    try:
        name=title.upper()
        def remove_spaces_variants(s):
            variants = set()
            for i in range(len(s) + 1):
                variant = s[:i] + s[i:].replace(" ", "")
                variants.add(variant)
            return variants

        def is_not_in_list(input_string, string_list):
            input_variants = remove_spaces_variants(input_string.replace(" ", ""))
            
            for string in string_list:
                list_variants = remove_spaces_variants(string.replace(" ", ""))
                if any(variant in list_variants for variant in input_variants):
                    return False
            return True

        allowed = is_not_in_list(name, string_list=COLUMN_VALUE)

        if allowed:
            return CommonResponse(
                status="success",
                input_title=name,
                isValid=True,
                invalid_words=[],
                message=f"{name} is allowed !",
            )
        else:
            return CommonResponse(
                status="success",
                input_title=name,
                isValid=False,
                invalid_words=[],
                message=f"{name} is not allowed !",
            )

    except Exception as e:
        return CommonResponse(
                status="failed",
                input_title=name,
                isValid=False,
                invalid_words=[],
                error=f"Internal Server Error {e}"
            )