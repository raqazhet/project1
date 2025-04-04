import logging
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from ..schema.transcript import TranslateSchema



class TransLateRepo:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.translate_collection: AsyncIOMotorCollection = db.translate

    async def create_translate_data(self,tr_data:dict)->str:
        try:
            result = await self.translate_collection.insert_one(tr_data)
            return str(result.inserted_id)
        except Exception as e:
            logging.error(f"Error creating translate: {e}")
            return ""

    async def get_translates_by_query(self, query: dict):
        try:
            result = []
            cursor = self.translate_collection.find(query)
            async for tr_data in cursor:
                tr_data['id'] = str(tr_data.pop('_id'))
                result.append(TranslateSchema(**tr_data))
            return result
        except Exception as e:
            logging.error(f"Error getting translates by query: {e}")
            return []

    async def get_translate_by_id(self, _id: str) -> TranslateSchema:
        try:
            result = await self.translate_collection.find_one({"_id": ObjectId(_id)})
            if result:
                result['id'] = str(result.pop('_id'))
                return TranslateSchema(**result)
            else:
                return TranslateSchema()
        except Exception as e:
            logging.error(f"Error getting translate by ID: {e}")
            return TranslateSchema()

    async def update_translate(self, _id: str, update_data: dict) -> TranslateSchema:
        try:
            result = await self.translate_collection.update_one({"_id": ObjectId(_id)},
                                                                 {"$set": update_data})
            if result.matched_count > 0:
                data = await self.translate_collection.find_one({"_id": ObjectId(_id)})
                return TranslateSchema(**data)
            else:
                return TranslateSchema()
        except Exception as e:
            logging.error(f"Error updating translate: {e}")
            return ""

    async def delete_translate_by_id(self, _id: str) -> str:
        try:
            result = await self.translate_collection.delete_one({"_id": ObjectId(_id)})
            if result.deleted_count > 0:
                return _id
            else:
                return ""
        except Exception as e:
            logging.error(f"Error deleting translate by ID: {e}")
            return ""

    


