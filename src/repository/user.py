from typing import List, Dict, Any
import logging
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from bson import ObjectId

from ..exceptions.user import UserAlreadyExist
from ..schema.user import UserResponse

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.users_collection: AsyncIOMotorCollection = db.users


    async def create_user(self, user_data: dict) -> str:
        try:
            # Check if user with the same email already exists
            existing_user = await self.users_collection.find_one({"email": user_data['email']})
            if existing_user:
                raise UserAlreadyExist
            # Insert the new user
            result = await self.users_collection.insert_one(user_data)
            # Check if the user was successfully inserted
            if result.inserted_id:
                logging.info("User created successfully.")
                return str(result.inserted_id)
            else:
                logging.error("Failed to create user. Inserted ID not found.")
                raise Exception("Failed to create user")
        except UserAlreadyExist:
            # Handle UserAlreadyExist exception
            logging.error("User with the specified email already exists.")
            raise

        except Exception as e:
            # Handle other exceptions
            logging.error(f"Error during user creation: {e}")
            raise Exception("Failed to create user")

    async def get_user_by_id(self, user_id: str) -> UserResponse:
        result = await self.users_collection.find_one({"_id": ObjectId(user_id)})
        if result:
            result["id"] = str(result.pop("_id"))
            result.pop('password')
            return UserResponse(**result)
        else:
            return None
    
    async def get_user_by_email(self,email:str)->UserResponse:
        user = await self.users_collection.find_one({"email":email})
        if user:
            user['id']= str(user.pop('_id'))
            user.pop('password')
            return UserResponse(**user)
        else:
            return None

    async def get_all_users(self) -> List[UserResponse]:
        result = self.users_collection.find({})
        users = []
        async for user in result.limit(10):
            user["id"] = str(user.pop("_id"))
            user.pop('password')
            users.append(UserResponse(**user))
        return users

    async def delete_user_by_id(self, user_id: str) -> str:
        result = await self.users_collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count > 0:
            return user_id
        else:
            return ""

    async def update_user(self,id:str, user_data: Dict[str, Any]) -> str:
        result = await self.users_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": user_data},
        )
        if result.matched_count > 0:
            return id
        else:
            logging.error("update user err: ")
            return ""