from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, FileResponse
from typing import List
from bs4 import BeautifulSoup
import random
import pandas as pd
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
from metaphone import doublemetaphone

from config.database import get_collection

trademark_router = APIRouter(prefix="/trademark", tags=["trademark"])



@trademark_router.get("/alldata")
async def get_all_data(
    limit: int = Query(50, description="Number of records to return"),
    show_soundex: bool = Query(False, description="Show Soundex Name"),
    show_metaphone: bool = Query(False, description="Show Metaphone Name"), 
    show_double_metaphone_primary: bool = Query(False, description="Show Double Metaphone Primary"),
    show_double_metaphone_secondary: bool = Query(False, description="Show Double Metaphone Secondary"),
    show_nysiis: bool = Query(False, description="Show NYSIIS Name")
):
    try:
        collection = get_collection("Alphabetic_sort")
        
        # Title_Name and Title_Code are always included
        output_fields = ["Title_Name", "Title_Code"]
        
        # Add optional fields based on query parameters
        if show_soundex:
            output_fields.append("Soundex_Name")
        if show_metaphone:
            output_fields.append("Metaphone_Name")
        if show_double_metaphone_primary:
            output_fields.append("Double_Metaphone_Primary")
        if show_double_metaphone_secondary:
            output_fields.append("Double_Metaphone_Secondary") 
        if show_nysiis:
            output_fields.append("NYSIIS_Name")

        data = collection.query(expr="", limit=limit, output_fields=output_fields, output_fields_exclude=["Auto_id"])
        return {"message": "data received successfully", "data": data}
    except Exception as e:
        return {"error": str(e)}, 500

