from datetime import datetime
import time
from ..repository.transcript import TranscriptRepo
from ..model.transcript import TranscriptCreate,UpdateTranscript
from ..schema.transcript import TrascriptSchema
from ..exceptions.transcript import TranscriptNotFoundById
from ..utils.utils import convert_georgia_time_to_hijri



class TranscriptService:
    def __init__(self,repository:TranscriptRepo) -> None:
        self.repo= repository

    async def create_transcrip(self,data:TranscriptCreate)->str:
        tr_data = data.dict()
        tr_data['created']=int(datetime.utcnow().timestamp())
        tr_data['updated']=int(datetime.utcnow().timestamp())
        tr_data['hijri_time']= await convert_georgia_time_to_hijri(tr_data['created'])
        id =await self.repo.create_transcript(tr_data=tr_data)
        if id:
            return id
        else:
            raise Exception('create transcript err')
    
    async def get_transcript_by_id(self,id:str)->TrascriptSchema:
        result = await self.repo.get_transcript_by_id(id)
        if result:
            return result
        else:
            raise TranscriptNotFoundById
        
    async def get_transcript_by_query(self,query:dict):
        result = await self.repo.get_transcript_by_query(query=query)
        return result
    
    async def delete_transcript(self,id:str)->str:
        id = await self.repo.delete_transcript_by_id(id)
        if id !="":
            return id
        else:
            raise TranscriptNotFoundById
        
    async def update_transcrip_data(self,id:str,data:UpdateTranscript)->TrascriptSchema:
        tr_data = data.dict()
        for key,val in tr_data:
            if val not in ["","string"]:
                tr_data[key]=val
        tr_data['updated']=int(datetime.utcnow().timestamp())
        result = await self.repo.update_transcript(id,tr_data)
        if result !=None:
            return result
        else:
            raise TranscriptNotFoundById