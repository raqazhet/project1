import json
from redis.asyncio import Redis
from .config.config import (REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,REDIS_DB)

# Создание подключения к Redis
redis_db = Redis(
    host=REDIS_HOST, port=REDIS_PORT, 
    password=REDIS_PASSWORD, db=REDIS_DB,
    decode_responses=True
)
async def redis_get(key: str):
    data = await redis_db.get(key)
    if data !=None:
        data = json.loads(data)
    return data
    

# Assuming redis_db is an instance of Redis
async def redis_set(key: str, val: dict):
    ttl = 900
    # Set the value using json.dumps()
    await redis_db.set(key, json.dumps(val))
    # Set the expiration using the expire method
    await redis_db.expire(key, ttl)


async def redis_set_daily_quote(key:str,val:dict):
    ttl = 86400
    # Set the value using json.dumps()
    await redis_db.set(key, json.dumps(val))
    # Set the expiration using the expire method
    await redis_db.expire(key, ttl)
    
async def redis_delete( key: str):
    await redis_db.delete(key)

async def redis_delete_for_celery(key:str):
    await redis_db.delete(key)
