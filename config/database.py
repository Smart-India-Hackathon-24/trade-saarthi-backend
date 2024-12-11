from pymilvus import Collection, connections, FieldSchema, CollectionSchema, DataType,MilvusClient
from dotenv import load_dotenv
load_dotenv()
import os

# Database Configuration
ZILLIZ_URI = os.getenv("ZILLIZ_URI")
ZILLIZ_TOKEN = os.getenv("ZILLIZ_TOKEN")

def connect_db():
    connections.connect(
        alias="default",
        uri=ZILLIZ_URI,
        token=ZILLIZ_TOKEN
    )
    
    if connections.has_connection("default"):
        print("Database connection successful!")
    else:
        print("Failed to connect to database")

def get_collection(collection_name):
    
    # schema = CollectionSchema(
    #     fields=[
    #         FieldSchema(name="Auto_id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    #         FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=384),
    #         FieldSchema(name="Title_Code", dtype=DataType.VARCHAR, max_length=200),
    #         FieldSchema(name="Title_Name", dtype=DataType.VARCHAR, max_length=200),
    #         FieldSchema(name="Soundex_Name", dtype=DataType.VARCHAR, max_length=200),
    #         FieldSchema(name="Metaphone_Name", dtype=DataType.VARCHAR, max_length=200),
    #         FieldSchema(name="Double_Metaphone_Primary", dtype=DataType.VARCHAR, max_length=200),
    #         FieldSchema(name="Double_Metaphone_Secondary", dtype=DataType.VARCHAR, max_length=200),
    #         FieldSchema(name="NYSIIS_Name", dtype=DataType.VARCHAR, max_length=200),
    #     ],
    #     description="Collection for trademark information"
    # )
    
    try:
        collection = Collection(collection_name)
        # collection = Collection(name=collection_name)
        # collection.load()
        return collection
    except Exception as e:
        # return Collection(name=collection_name, schema=schema)
        return {"error": str(e)}