import logging
from typing import List
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from ..schema.ayah import AyahSchema

class AyahRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.ayah_collection: AsyncIOMotorCollection = db.ayah

    async def create_ayah(self, ayah_data: dict) -> str:
        try:
            result = await self.ayah_collection.insert_one(ayah_data)
            if result.inserted_id:
                return str(result.inserted_id)
            else:
                return ""
        except Exception as e:
            logging.error("create ayah err: ",e)
            # Handle the exception (e.g., log it)
            return ""

    async def get_ayah_by_id(self, ayah_id: str) -> AyahSchema:
        try:
            result = await self.ayah_collection.find_one({"_id": ObjectId(ayah_id)})
            if result:
                result['id'] = str(result.pop('_id'))
                return AyahSchema(**result)
            else:
                return AyahSchema()
        except Exception as e:
            logging.error('get ayah by id err: ',e)
            # Handle the exception (e.g., log it)
            return AyahSchema()

    async def get_all_ayahs(self, query: dict) -> List[AyahSchema]:
        try:
            ayahs = []
            cursor = self.ayah_collection.find(query)
            async for ayah in cursor:
                ayah['id'] = str(ayah.pop('_id'))
                ayahs.append(AyahSchema(**ayah))
            return ayahs
        except Exception as e:
            logging.error('get all ayah err: ',e)
            # Handle the exception (e.g., log it)
            return []

    async def update_ayah(self, ayah_id: str, update_data: dict) -> dict:
        try:
            result = await self.ayah_collection.update_one(
                {"_id": ObjectId(ayah_id)},
                {"$set": update_data}
            )
            if result.matched_count > 0:
                return await self.ayah_collection.find_one({"_id": ObjectId(ayah_id)})
            else:
                return {}
        except Exception as e:
            logging.error('update ayah err: ',e)
            # Handle the exception (e.g., log it)
            return {}

    async def delete_ayah(self, ayah_id: str) -> str:
        try:
            result = await self.ayah_collection.delete_one({"_id": ObjectId(ayah_id)})
            if result.deleted_count > 0:
                return ayah_id
            else:
                return ""
        except Exception as e:
            logging.error('delete ayah err: ',e)
            # Handle the exception (e.g., log it)
            return ""
