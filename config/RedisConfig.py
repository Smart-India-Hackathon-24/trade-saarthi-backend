from redis import Redis
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Redis Configuration
redis_client = Redis(
    host=os.getenv("REDISHOST", "localhost"),
    port=int(os.getenv("REDISPORT", 6379)),
    password=os.getenv("REDISPASSWORD", ""),
    db=int(os.getenv("REDISDB", 0)),
    decode_responses=True
)

def get_redis_client():
    return redis_client
