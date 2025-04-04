from datetime import datetime
# from hijri_converter import convert

from ..repository.hadith import HadithRepo
from ..model.hadith import HadithCreate,HadithUpdate
from ..schema.hadith import HadithSchema
from ..exceptions.hadith import HadithNotFoundById
from ..utils.utils import convert_georgia_time_to_hijri



class Hadithservice:
    def __init__(self,repo :HadithRepo) -> None:
        self.repo= repo

    async def create_hadith(self,data:HadithCreate)->str:
        h_data =data.dict()
        created = int(datetime.utcnow().timestamp())
        h_data['created']=created
        h_data['updated']= created
        h_data['hijri_time']=await convert_georgia_time_to_hijri(created)
        id = await self.repo.create_hadith(h_data)
        if id != "":
            return id
        else:
            raise Exception("Create hadith error")
        
    async def get_hadith_by_id(self,id : str)->HadithSchema:
        data = await self.repo.get_hadith_by_id(id=id)
        if data != None:
            return data
        else:
            raise HadithNotFoundById
    
    async def get_all_hadith_by_query(self,query:dict)->list[HadithSchema]:
        hadithes = await self.repo.get_all_hadith_by_query(query=query)
        return hadithes
    
    async def delete_hadith_by_id(self,id:str):
       deleted_id = await self.repo.delete_hadith_by_id(id=id)
       if deleted_id:
           return deleted_id
       else:
           raise HadithNotFoundById

    async def update_hadith_by_id(self,id:str,data:HadithUpdate):
        updated_data = data.dict()
        for key, val in updated_data.items():  # Use items() to iterate over key-value pairs
            if val not in ["", "string"]:
                updated_data[key] = val
        result = await self.repo.update_hadith_data(id,updated_data)
        if result:
            return result
        else:
            raise HadithNotFoundById 