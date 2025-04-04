from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from ..schema.like import LikeResponse

class LikeRepo:
    def __init__(self,db:AsyncIOMotorDatabase) -> None:
        self.like_collection :AsyncIOMotorCollection = db.likes

    async def create_like(self,data:dict)->str:
        delete_data =await self.like_collection.find_one({"client_id":data['client_id'],
                                                     "card_id":data['card_id']})
        if delete_data:
            await self.like_collection.delete_one({"_id":delete_data['_id']})
        result = await self.like_collection.insert_one(data)
        if result.inserted_id:
            return str(result.inserted_id)
        else:
            return ""
        
    async def get_like_by_id(self,id:str)->LikeResponse:
        result = await self.like_collection.find_one({"_id":ObjectId(id)})
        if result:
            result['id']=str(result.pop('_id'))
            return LikeResponse(**result)
        else:
            return LikeResponse()
        
    async def get_all_likes_by_query(self,query:dict)->list[LikeResponse]:
        result = self.like_collection.find(query)
        likes =[]
        async for like in result:
            like['id']=str(like.pop('_id'))
            likes.append(LikeResponse(**like))
        return likes
    