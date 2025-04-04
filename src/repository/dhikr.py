import logging
from fastapi import HTTPException
from typing import List
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from ..schema.ayah import AyahSchema

class DhikrRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.dhikr_collection: AsyncIOMotorCollection = db.dhikr

    async def create_dhikr(self,data:dict)->str:
        result = await self.dhikr_collection.insert_one(data)
        if result.inserted_id:
            return str(result.inserted_id)
        else:
            return ""
        
    async def get_dhikr_by_id(self,id:str):
        result = await self.dhikr_collection.find_one({"_id":ObjectId(id)})
        if result:
            result['id']=str(result.pop('_id'))
            return result
        else:
            raise HTTPException(status_code=400,detail="bad request")
        
    async def delete_dhikr_by_id(self,id:str):
        result = await self.dhikr_collection.delete_one({"_id":ObjectId(id)})
        if result.deleted_count>0:
            return id
        else:
            raise HTTPException(status_code=400,detail="dhikr not found by id")
        
    async def get_all_dhikr(self,query:dict):
        dhikrs =[]
        result = self.dhikr_collection.find(query)
        async for dhikr in result:
            dhikr['id']=str(dhikr.pop('_id'))
            dhikrs.append(dhikr)
        return dhikrs