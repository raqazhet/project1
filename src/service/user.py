from typing import List
from datetime import datetime
from fastapi import HTTPException
from ..repository.user import UserRepository
from ..exceptions.user import UserNotFound
from ..schema.user import UserResponse
from ..model.user import UserCreate
from ..utils.utils import (
    hash_password,verify_password,convert_georgia_time_to_hijri,
    create_access_token,create_refresh_token)

# from  import BookRepository
# from schemas.books import Book


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def sing_in_logic(self,user_data:dict)->dict:
        user = await self.repository.get_user_by_email(user_data['email'])
        if user ==None:
            raise UserNotFound
        if  verify_password(user_data['password'],hashed_password=user.hash_password) !=True:
            raise HTTPException(status_code=400,detail="Email or password is incorrect!")
        access_token = await create_access_token(user.id)
        refresh_token = await create_refresh_token(user.id)
        token_data ={
            "access_token":access_token,
            "refresh_token":refresh_token
        }    
        return token_data


    async def get_all_user(self) -> List[UserResponse]:
        result =await  self.repository.get_all_users()
        return result

    async def create_user(self,user:UserCreate) ->str:
        user_data = user.dict()
        user_data["created"] = int(datetime.now().timestamp())
        user_data["hash_password"]=hash_password(user_data['password'])
        user_data['updated']=0
        user_data['hijri_time']=await convert_georgia_time_to_hijri(user_data['created'])
        user_data['last_read_zikrid']=0
        user_data['role']='client'
        id =await self.repository.create_user(user_data=user_data)
        if id:
            return id
        else:
            raise Exception
        
    async def get_user_id(self,id:str)->UserResponse:
        result = await self.repository.get_user_by_id(user_id=id)
        if result !=None:
            return result
        else:
            raise UserNotFound
        
    async def delete_user_bu_id(self,id:str):
        result = await self.repository.delete_user_by_id(user_id=id)
        if result:
            return result
        else:
            raise UserNotFound
        
    async def update_user_data(self,id:str,user:dict)->str:
        for key,val in user.items():
            if val not in ["","string"]:
                user[key]=val
        user['updated']=int(datetime.utcnow().timestamp())
        result = await self.repository.update_user(id=id,user_data=user)
        if result:
            return result
        else:
            raise UserNotFound
        