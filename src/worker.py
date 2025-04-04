from celery import Celery
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from datetime import date, timedelta,datetime
import json
import asyncio
from .config.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD
from .repository.db import get_database
from .redis import redis_set_daily_quote, redis_delete_for_celery

celery = Celery(__name__)

# Configure Celery broker and result backend
broker_url = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
result_backend = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
celery.conf.update(
    broker_url=broker_url,
    result_backend=result_backend,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Calculate the current time + 3 minutes
now = datetime.utcnow() + timedelta(minutes=3)
minute = now.minute
hour = now.hour
# Schedule tasks using beat_schedule
celery.conf.beat_schedule = {
    "update-daily-quote": {
        "task": "tasks.update_daily_quote",  # Adjust the task name if needed
        "schedule": crontab(minute=0, hour=0),  # Run every day at 00:00 UTC
    },
}


logger = get_task_logger(__name__)


@celery.task(name='tasks.update_daily_quote')
def update_daily_quote():
    loop = asyncio.get_event_loop()

    collections = ["ayah", "hadith", "dhikr", "file"]  # Replace with your list of topics
    for collection in collections:
        yesterday_iso = date.today() - timedelta(days=1)
        key = f"{yesterday_iso.isoformat()}_{collection}"
        loop.run_until_complete(redis_delete_for_celery(key=key))
        try:
            loop.run_until_complete(get_and_save_daily_quote(collection))
        except Exception as e:
            logger.error(f"Error updating daily quote for {collection}: {e}")

# Your existing asynchronous function
async def get_and_save_daily_quote(collection_name: str):
    db = get_database()
    random_quote = await db[collection_name].aggregate([{ "$sample": { "size": 1 } }]).to_list(length=1)
    if random_quote:
        res = random_quote[0]
        res['id']=str(res.pop('_id'))
        today = date.today().isoformat()
        json_serializable_res = json.loads(json.dumps(res, default=str))
        await redis_set_daily_quote(f"{today}_{collection_name}", json_serializable_res)
    else:
        raise Exception(f"Failed to fetch a random quote for topic: {collection_name}")