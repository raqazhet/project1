import logging
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from ..schema.transcript import TrascriptSchema

class TranscriptRepo:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.transcript_collection: AsyncIOMotorCollection = db.transcript

    async def create_transcript(self, tr_data: dict) -> str:
        try:
            result = await self.transcript_collection.insert_one(tr_data)
            return str(result.inserted_id)
        except Exception as e:
            logging.error(f"Error creating transcript: {e}")
            return ""

    async def get_transcript_by_query(self, query: dict):
        try:
            result = []
            cursor = self.transcript_collection.find(query)
            async for tr_data in cursor:
                tr_data['id'] = str(tr_data.pop('_id'))
                result.append(TrascriptSchema(**tr_data))
            return result
        except Exception as e:
            logging.error(f"Error getting transcripts by query: {e}")
            return []

    async def get_transcript_by_id(self, _id: str) -> TrascriptSchema:
        try:
            result = await self.transcript_collection.find_one({"_id": ObjectId(_id)})
            if result:
                result['id'] = str(result.pop('_id'))
                return TrascriptSchema(**result)
            else:
                return TrascriptSchema()
        except Exception as e:
            logging.error(f"Error getting transcript by ID: {e}")
            return TrascriptSchema()

    async def update_transcript(self, _id: str, update_data: dict) -> TrascriptSchema:
        try:
            result = await self.transcript_collection.update_one({"_id": ObjectId(_id)},
                                                                 {"$set": update_data})
            if result.matched_count > 0:
                data = await self.transcript_collection.find_one({"_id": ObjectId(_id)})
                return TrascriptSchema(**data)
            else:
                return TrascriptSchema()
        except Exception as e:
            logging.error(f"Error updating transcript: {e}")
            return ""

    async def delete_transcript_by_id(self, _id: str) -> str:
        try:
            result = await self.transcript_collection.delete_one({"_id": ObjectId(_id)})
            if result.deleted_count > 0:
                return _id
            else:
                return ""
        except Exception as e:
            logging.error(f"Error deleting transcript by ID: {e}")
            return ""
