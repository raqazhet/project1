from datetime import datetime
import time
from ..repository.translate import TransLateRepo
from ..model.transcript import TranslateCreate,TransLateUpdate
from ..schema.transcript import TranslateSchema
from ..exceptions.transcript import TransLateNotFound
from ..utils.utils import convert_georgia_time_to_hijri



class TransLateService:
    def __init__(self,repository:TransLateRepo) -> None:
        self.repo= repository

    async def create_translate(self,data:TranslateCreate)->str:
        tr_data = data.dict()
        tr_data['created']=int(datetime.utcnow().timestamp())
        tr_data['updated']=int(datetime.utcnow().timestamp())
        tr_data['hijri_time']= await convert_georgia_time_to_hijri(tr_data['created'])
        id =await self.repo.create_translate_data(tr_data=tr_data)
        if id:
            return id
        else:
            raise Exception('create transcript err')
    
    async def get_transcript_by_id(self,id:str)->TranslateSchema:
        result = await self.repo.get_translate_by_id(id)
        if result:
            return result
        else:
            raise TransLateNotFound
        
    async def get_transcript_by_query(self,query:dict):
        result = await self.repo.get_translates_by_query(query=query)
        return result
    
    async def delete_transcript(self,id:str)->str:
        id = await self.repo.delete_translate_by_id(id)
        if id !="":
            return id
        else:
            raise TransLateNotFound
        
    async def update_transcrip_data(self,id:str,data:TransLateUpdate)->TranslateSchema:
        tr_data = data.dict()
        for key,val in tr_data:
            if val not in ["","string"]:
                tr_data[key]=val
        tr_data['updated']=int(datetime.utcnow().timestamp())
        result = await self.repo.update_transcript(id,tr_data)
        if result !=None:
            return result
        else:
            raise TransLateNotFound