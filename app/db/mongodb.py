import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI environment variable not set")

client = AsyncIOMotorClient(MONGODB_URI)

db = client["leeMuscatDB"]
