from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, add_pagination,paginate
from dataclasses import asdict

from ..redis import redis_get,redis_set,redis_delete
from ..dependencies import get_user_service,get_current_user
from ..schema.user import UserResponse
from ..service.user import UserService
from ..model.user import UserUpdate


user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/", response_model=Page[UserResponse])
async def get_all_users(
    current_user: UserResponse = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You don't have permission")

    users = await service.get_all_user()
    return paginate(users)


@user_router.get("/{id}",response_model=dict)
async def get_user_by_id(id:str,
                        #  redis:Redis=Depends(get_redis),
                        current_user: UserResponse = Depends(get_current_user),
                        service: UserService = Depends(get_user_service)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="You don't have permission")
    key =f"user:{id}"
    user_data = await redis_get(key=key)
    if user_data !=None:
        return {"result":user_data}
    user = await service.get_user_id(id=id)
    await redis_set(key,asdict(user))
    return {"result":user}


@user_router.put("/{user_id}",response_model=dict)
async def update_user_data(user_id:str,
                           data:UserUpdate,
                           current_user: UserResponse = Depends(get_current_user),
                        service: UserService = Depends(get_user_service)):
    user_data = data.dict()
    key = f"user:{user_id}"
    result = await service.update_user_data(id=user_id,user=user_data)
    await redis_delete(key=key)
    user_data= await service.get_user_id(id=user_id)
    await redis_set(key=key,val=asdict(user_data))
    return {"result":result}    

@user_router.delete("/{id}",response_model=dict)
async def delete_user_by_id(id:str,
                             current_user: UserResponse = Depends(get_current_user),
                             service: UserService = Depends(get_user_service)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="You don't have permission")
    deleted_id = await service.delete_user_bu_id(id=id)
    key =f"user:{id}"
    await redis_delete(key=key)
    return {"sucess":f"successfully deleted user by id: {deleted_id}"}

    


add_pagination(user_router)  # Add this line to enable pagination for this router