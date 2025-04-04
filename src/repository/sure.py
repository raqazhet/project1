from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase,AsyncIOMotorCollection



class SureRepo:
    def __init__(self,db:AsyncIOMotorDatabase) -> None:
        self.sure_collection :AsyncIOMotorCollection=db.sure

    async def create_sure(self,sure_data:dict)->str:
        result = await self.sure_collection.insert_one(sure_data)
        if result.inserted_id:
            return str(result.inserted_id)
        else:
            return ""
    
    async def get_sure_by_id(self,id:str)->dict:
        result = await self.sure_collection.find_one({"_id":ObjectId(id)})
        if result:
            result['id']= str(result.pop('_id'))
            return result
        else:
            return ""
    
    async def get_all_sure_by_query(self,query:dict)->list[dict]:
        result = self.sure_collection.find(query)
        sures =[]
        async for sure in result:
            sure['id']=str(sure.pop('_id'))
            sures.append(sure)
        return sures
    
    async def update_sure(self,sure_data:dict)->str:
        result = await self.sure_collection.update_one({"_id":ObjectId(sure_data[id])},
                                                       {"$set":sure_data})
        if result.matched_count>0:
            return sure_data['id']
        else:
            return ""
        
    async def delete_sure_by_id(self,id:str)->str:
        result = await self.sure_collection.delete_one({"_id":ObjectId(id)})
        if result.deleted_count>0:
            return id
        else:
            return ""