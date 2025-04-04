from datetime import datetime
# from typing import Any
# from time import 
from fastapi import HTTPException
from ..repository.ayah import AyahRepository
from ..model.ayah import AyahCreate
from ..exceptions.ayah import AyahNotFound
from ..utils.utils import convert_georgia_time_to_hijri


class AyahService:
    def __init__(self,repository:AyahRepository) -> None:
        self.repo =repository

    async def create_ayah(self,data:AyahCreate)->str:
        ayah_data = data.dict()
        ayah_data['created']=int(datetime.now().timestamp())
        ayah_data['updated']=0
        ayah_data['hijri_time']=await convert_georgia_time_to_hijri(ayah_data['created'])
        result = await self.repo.create_ayah(ayah_data=ayah_data)
        if result !="":
            return result
        else:
            raise HTTPException(status_code=500,detail="Error in create ayah logic")
        
    async def get_ayah_by_id(self,id:str):
        result = await self.repo.get_ayah_by_id(ayah_id=id)
        if result !=None:
            return result
        else:
            raise AyahNotFound
        
    async def get_all_ayahs(self,data:dict):
        result = await self.repo.get_all_ayahs(data)
        return result

    async def delete_ayah_by_id(self,id:str)->str:
        ayah_id = await self.repo.delete_ayah(ayah_id=id)
        if ayah_id !="":
            return ayah_id
        else:
            raise AyahNotFound
