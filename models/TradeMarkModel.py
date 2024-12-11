from pydantic import BaseModel
from typing import List

class TrademarkData(BaseModel):
    vector_of_metaphone:List[float]
    vector_of_name:List[float]
    vector_of_metaphone_without_sorting:List[float]
    title_code: str
    title_name: str
    title_name_after_sort: str 
    metaphone_name_after_sort: str 
    metaphone_name_without_sorting: str 

    class Config:
        schema_extra = {
            "example": {
                "vector_of_metaphone": [0.1, 0.2, 0.3],
                "vector_of_name": [0.4, 0.5, 0.6],
                "vector_of_metaphone_without_sorting": [0.7, 0.8, 0.9],
                "title_code": "XYZ789",
                "title_name": "Example Trademark",
                "title_name_after_sort": "Example Trademark",
                "metaphone_name_after_sort": "Exmpl Trdmrk",
                "metaphone_name_without_sorting": "ExmplTrdmrk",
            }
        }