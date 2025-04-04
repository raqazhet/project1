from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from ..schema.file import FileSchema


class FileRepo:
    def __init__(self,db:AsyncIOMotorDatabase) -> None:
        self.file_collection :AsyncIOMotorCollection=db.file

    
    async def create_file(self,data:dict)->str:
        result = await self.file_collection.insert_one(data)
        if result.inserted_id:
            return str(result.inserted_id)
        else:
            return ""
        
    async def get_file_by_id(self,id:str)->FileSchema:
        result = await self.file_collection.find_one({"_id":ObjectId(id)})
        if result:
            result['id']=str(result.pop('_id'))
            return FileSchema(**result)
        else:
            raise FileSchema()
        
    async def delete_file_by_id(self,id:str)->str:
        result = await self.file_collection.delete_one({"_id":ObjectId(id)})
        if result.deleted_count>0:
            return id
        else:
            return ""