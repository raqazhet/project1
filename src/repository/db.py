# Installed packages
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
# from motor.motor_asyncio import unique_index
##Local packages
from ..config.config import MONGO_DB
from ..utils.utils import convert_georgia_time_to_hijri

logger = logging.getLogger(__name__)

# MongoDB connection
client = AsyncIOMotorClient(MONGO_DB)
db = client['sajda_db']

def get_database(): 
    return db


async def setup_db():
    users_collection = db['users']
    users_collection.create_index("email", unique=True)
    created_time = int(datetime.utcnow().timestamp())
    hijri_time =await convert_georgia_time_to_hijri(created_time)

    _data = {
        "firstname": "admin",
        "lastname": "admin",
        "email": "admin@example.com",
        "created": created_time,
        "updated": created_time,
        "last_read_zikrid": "12313",
        "password":"admin",
        "hash_password": "$2b$12$nQYUGEW9UZY.lqtnezL9AOOD3mlBxwIyCy6q.WB7LUJcGIBg9Qfr6",  # Replace with the actual hashed password
        "phone_number": "1234567890",
        "region": "default_region",
        "role": "admin",
        "hijri_time":hijri_time
    }
    await users_collection.insert_one(_data)
    # Perform necessary operations with _data
