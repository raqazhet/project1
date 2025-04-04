from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase,AsyncIOMotorCollection

from ..schema.hadith import HadithSchema


class HadithRepo:
    def __init__(self,db:AsyncIOMotorDatabase) -> None:
        self.hadith_collection :AsyncIOMotorCollection= db.hadith
    
    async def create_hadith(self,data:dict):
        result = await self.hadith_collection.insert_one(data)
        if result.inserted_id:
            return str(result.inserted_id)
        else:
            return ""

    async def get_all_hadith_by_query(self,query:dict)->list[HadithSchema]:
        results=[]
        result = self.hadith_collection.find(query)
        async for hadith in result:
            hadith['id']=str(hadith.pop('_id'))
            results.append(HadithSchema(**hadith))
        return results
    
    async def get_hadith_by_id(self,id:str)->HadithSchema:
        result = await self.hadith_collection.find_one({'_id':ObjectId(id)})
        if result:
            result['id']= str(result.pop('_id'))
            return HadithSchema(**result)
        else:
            return None
        
    async def delete_hadith_by_id(self,id):
        result = await self.hadith_collection.delete_one({"_id":ObjectId(id)})
        if result.deleted_count>0:
            return id
        else:
            return ""
        
    async def update_hadith_data(self,id: str,update_data:dict)->HadithSchema:
        result = await self.hadith_collection.update_one({"_id":ObjectId(id)},
                                                         {"$set":update_data})
        if result.matched_count > 0:
            data = await self.hadith_collection.find_one({'_id':ObjectId(id)})
            data['id']=str(data.pop('_id'))
            return HadithSchema(**data)
        else:
            return None