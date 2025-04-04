from ..repository.likes import LikeRepo
from ..model.likes import LikeCreate,UpdateLike
from fastapi import HTTPException

class LikeService:
    def __init__(self,repo:LikeRepo) -> None:
        self.repo =repo

    async def create_like(self,client_id:str,data:LikeCreate)->str:
        if data.card_type not in ["hadith","ayah","dhikr"]:
            raise HTTPException(status_code=400,detail="card type is not allowed")
        
        data=data.dict()
        data['client_id']=client_id
        data['updated']=0
        result = await self.repo.create_like(data=data)
        if result:
            return result
        else:
            raise Exception('create like error')
    
    async def get_like_by_id(self,id:str):
        result = await self.repo.get_like_by_id(id=id)
        if result !=None:
            return result
        else:
            raise HTTPException(status_code=400,detail="like not found by id")
        
    async def get_all_likes_by_query(self,query:dict):
        resukt = await self.repo.get_all_likes_by_query(query=query)
        return resukt
    
    async def update_like_by_id(self,id:str,data:UpdateLike):
        pass