from fastapi import APIRouter,HTTPException,Depends
from fastapi_pagination import Page, add_pagination,paginate
from dataclasses import asdict
from datetime import date
from ..model.ayah import DHikrCreate
from ..dependencies import get_dhikr_service,get_current_user,get_user_service
from ..schema.user import UserResponse
from ..service.dhikr import DhikrService
from ..service.user import UserService
from ..redis import redis_get,redis_set,redis_delete


dhikr_router = APIRouter(prefix="/dhikr",tags=['dhikr'])


@dhikr_router.post("/",response_model=dict)
async def create_dhikr(data:DHikrCreate,
                       current_user:UserResponse=Depends(get_current_user),
                       service:DhikrService=Depends(get_dhikr_service)):
    if current_user.role !='admin':
        raise HTTPException(status_code=403,detail="you don't have permission")
    res = await service.create_dhikr(data=data)
    return {"created_id":res}

@dhikr_router.get("/{id}",response_model=dict)
async def get_dhikr_by_id(id:str,
                          user_service:UserService=Depends(get_user_service),
                          current_user:UserResponse=Depends(get_current_user),
                       service:DhikrService=Depends(get_dhikr_service)):
    if current_user.role not in ['admin','client']:
        raise HTTPException(status_code=403,detail="you don't have access")
    _ = await user_service.update_user_data(current_user.id,{"last_read_zikrid":id})
    key = f"dhikr:{id}"
    dhikr_data = await redis_get(key=key)
    if dhikr_data:
        return{"result":dhikr_data}
    result =await service.get_dhikr_by_id(id)
    await redis_set(key=key,val=result)
    return {"result":result}


@dhikr_router.get("/",response_model=Page[dict])
async def get_all_dhikr(
                       service:DhikrService=Depends(get_dhikr_service)):
    result =await service.get_all_dhikr({})
    return paginate(result)

@dhikr_router.delete("/{id}",response_model=dict)
async def delete_dhikr_by_id(id:str,
                             current_user:UserResponse=Depends(get_current_user),
                       service:DhikrService=Depends(get_dhikr_service)):
    if current_user.role !='admin':
        raise HTTPException(status_code=403,detail="you don't have permission")
    del_id =await service.delete_dhikr_by_id(id)
    await redis_delete(f"dhikr:{id}")
    return {"result":del_id}


@dhikr_router.get("/dhikr/day",response_model=dict)
async def get_dhikr_of_day():
    key = f"{date.today().isoformat()}_dhikr"
    result = await redis_get(key=key)
    if not result:
        raise HTTPException(status_code=500,detail="celery beat doesn't work")
    return {"result":result}

add_pagination(dhikr_router)
