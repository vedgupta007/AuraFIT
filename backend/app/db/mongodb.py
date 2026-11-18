from motor.motor_asyncio import AsyncIOMotorClient
import logging
from app.core.config import settings
from pymongo import ASCENDING, DESCENDING

logger = logging.getLogger("uvicorn.error")

class Database:
    client: AsyncIOMotorClient = None
    client = None

db = Database()

async def connect_to_mongo():
    try:
        import os
        import re
        
        if settings.MONGODB_URI.startswith("mongodb+srv://"):
            logger.info("MongoDB Atlas configured")
        elif settings.MONGODB_URI.startswith("mongodb://"):
            logger.info("Local MongoDB configured")
        else:
            logger.warning("Unknown MongoDB URI scheme configured")
            
        # Check if we are running under pytest
        if os.getenv("TESTING") == "1":
            logger.info("Using mongomock_motor for testing")
            from mongomock_motor import AsyncMongoMockClient
            db.client = AsyncMongoMockClient()
        else:
            logger.info(f"Connecting to real MongoDB instance. DB Name: {settings.MONGODB_DB_NAME}")
            # Ensure normal dev does not use mongomock
            db.client = AsyncIOMotorClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
            # A quick ping to verify connection early
            await db.client.admin.command('ping')
            logger.info("MongoDB ping successful.")
            
        database = db.client[settings.MONGODB_DB_NAME]
        
        # Ensure indexes
        await database.users.create_index([("email", ASCENDING)], unique=True)
        await database.profiles.create_index([("user_id", ASCENDING)], unique=True)
        await database.meals.create_index([("user_id", ASCENDING)])
        await database.meals.create_index([("user_id", ASCENDING), ("consumed_at", ASCENDING)])
        
        # Phase 5: AI Conversations Index
        await database.ai_conversations.create_index([("user_id", ASCENDING), ("updated_at", DESCENDING)])
        
        # Phase 6 Core: Workouts, Goals, Measurements
        await database.workouts.create_index([("user_id", ASCENDING)])
        await database.workouts.create_index([("user_id", ASCENDING), ("started_at", DESCENDING)])
        await database.goals.create_index([("user_id", ASCENDING)])
        await database.measurements.create_index([("user_id", ASCENDING), ("date", DESCENDING)])
        
        logger.info("Indexes verified/created successfully.")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB or creating indexes: {e}")
        raise
        
    logger.info("MongoDB initialization complete.")

async def close_mongo_connection():
    logger.info("Closing MongoDB connection...")
    if db.client:
        db.client.close()
        # Mock client doesn't need to close
        if hasattr(db.client, "close"):
            db.client.close()
    logger.info("MongoDB connection closed")

def get_database():
    return db.client[settings.MONGODB_DB_NAME]
