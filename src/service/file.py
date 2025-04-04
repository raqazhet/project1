from datetime import datetime
from ..repository.file import FileRepo
from ..exceptions.hadith import FileNotFoundById


class FileService:
    def __init__(self,repository:FileRepo) -> None:
        self.repo = repository

    async def create_file(self,data:dict)->str:
        data['created']=int(datetime.utcnow().timestamp())
        result = await self.repo.create_file(data=data)
        if result !="":
            return result
        else:
            raise Exception("create file error")
        
    async def get_file_by_id(self,id:str):
        result = await self.repo.get_file_by_id(id=id)
        if result !=None:
            return result
        else:
            raise FileNotFoundById
        
    async def delete_file_by_id(self,id:str):
        result = await self.repo.delete_file_by_id(id)
        if result =="":
            raise FileNotFoundById
        else:
            return result