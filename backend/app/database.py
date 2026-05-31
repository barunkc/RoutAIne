"""
MongoDB database connection and initialization.

Manages database connection, collections, and utility functions.
"""

from motor.motor_asyncio import AsyncClient, AsyncDatabase
from app.config import settings
from typing import Optional

# Global database instance
_db: Optional[AsyncDatabase] = None


async def init_db() -> AsyncDatabase:
    """
    Initialize MongoDB connection.
    
    Returns:
        AsyncDatabase: Connected MongoDB database instance
    """
    global _db
    
    try:
        client = AsyncClient(settings.MONGODB_URL)
        _db = client[settings.DATABASE_NAME]
        
        # Verify connection
        await _db.command('ping')
        print(f"✓ Connected to MongoDB: {settings.DATABASE_NAME}")
        
        # Create indexes
        await create_indexes()
        
        return _db
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        raise


async def get_db() -> AsyncDatabase:
    """
    Get database instance.
    
    Returns:
        AsyncDatabase: Connected MongoDB database
    """
    if _db is None:
        await init_db()
    return _db


async def create_indexes():
    """Create database indexes for performance optimization."""
    db = await get_db()
    
    # Tasks collection indexes
    await db.tasks.create_index("deadline")
    await db.tasks.create_index("priority")
    await db.tasks.create_index("category")
    await db.tasks.create_index("createdAt")
    
    # Routines collection indexes
    await db.routines.create_index("date")
    await db.routines.create_index("generatedBy")
    
    # Habits collection indexes
    await db.habits.create_index("frequency")
    await db.habits.create_index("createdAt")
    
    # Notifications collection indexes
    await db.notifications.create_index("sentAt")
    await db.notifications.create_index("status")
    await db.notifications.create_index([("sentAt", -1)], expireAfterSeconds=2592000)  # 30 days TTL
    
    print("✓ Database indexes created")


async def close_db():
    """Close database connection."""
    global _db
    if _db is not None:
        _db.client.close()
        _db = None
        print("✓ Database connection closed")
