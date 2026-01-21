from motor.motor_asyncio import AsyncIOMotorClient
import os
import certifi  # <--- 1. Importe o certifi

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "app_db")

_client: AsyncIOMotorClient | None = None

def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        # 2. Adicione tlsCAFile=certifi.where() na criação do cliente
        _client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
    return _client

def get_database():
    return get_client()[MONGO_DB]

def get_user_collection():
    return get_database()["users"]