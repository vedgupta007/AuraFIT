import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.mongodb import connect_to_mongo, close_mongo_connection, get_database

def normalize_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("(", "").replace(")", "").replace(",", "")

async def fix_existing():
    await connect_to_mongo()
    db = get_database()
    
    # Update foods
    cursor = db.foods.find({"normalized_name": {"$exists": False}})
    async for doc in cursor:
        n_name = normalize_name(doc["name"] + "_" + str(doc.get("serving_size", 1)) + doc.get("serving_unit", ""))
        await db.foods.update_one({"_id": doc["_id"]}, {"$set": {"normalized_name": n_name}})
        
    # Update exercises
    cursor = db.exercises.find({"normalized_name": {"$exists": False}})
    async for doc in cursor:
        n_name = normalize_name(doc["name"])
        await db.exercises.update_one({"_id": doc["_id"]}, {"$set": {"normalized_name": n_name}})
        
    print("Existing documents normalized.")
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(fix_existing())
