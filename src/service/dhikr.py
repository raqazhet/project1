from datetime import datetime
# from typing import Any
# from time import 
from ..repository.dhikr import DhikrRepository
from ..model.ayah import DHikrCreate
from ..utils.utils import convert_georgia_time_to_hijri


class DhikrService:
    def __init__(self,repository:DhikrRepository) -> None:
        self.repo =repository

    async def create_dhikr(self,data:DHikrCreate)->str:
        dh_data = data.dict()
        dh_data['created']=int(datetime.utcnow().timestamp())
        dh_data['updated']=dh_data['created']
        dh_data['hijri_time'] = await convert_georgia_time_to_hijri(dh_data['created'])
        result = await self.repo.create_dhikr(data=dh_data)
        return result
    
    async def get_dhikr_by_id(self,id:str):
        result = await self.repo.get_dhikr_by_id(id=id)
        return result
    
    async def delete_dhikr_by_id(self,id:str):
        res = await self.repo.delete_dhikr_by_id(id=id)
        return res
    
    async def get_all_dhikr(self,query:dict):
        res =await self.repo.get_all_dhikr(query=query)
        return res