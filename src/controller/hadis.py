from fastapi import APIRouter, Depends,HTTPException
from fastapi_pagination import Page, add_pagination,paginate
from dataclasses import asdict
from datetime import date

from ..model.hadith import HadithCreate,HadithUpdate
from ..dependencies import get_current_user,get_hadith_service
from ..schema.user import UserResponse
from ..schema.hadith import HadithSchema
from ..service.hadith import Hadithservice
from ..exceptions.exception import PermissionException
from ..redis import redis_get,redis_set,redis_delete

hadis_router = APIRouter(prefix="/hadith",tags=["hadith"])

@hadis_router.post("/",response_model=dict)
async def create_hadith(data:HadithCreate,
                        current_user:UserResponse=Depends(get_current_user),
                        service:Hadithservice=Depends(get_hadith_service)):
    if current_user.role !="admin":
        raise PermissionException
    id = await service.create_hadith(data=data)
    return {"created_id":id}

@hadis_router.get("/{id}",response_model=dict)
async def get_hadith_by_id(id:str,
                           service:Hadithservice=Depends(get_hadith_service)):
    key =f"hadis:{id}"
    hadis_data = await redis_get(key=key)
    if hadis_data:
        return {"result":hadis_data}
    result = await service.get_hadith_by_id(id=id)
    await redis_set(key=key,val=asdict(result))
    return {"result":result}

@hadis_router.get("/",response_model=Page[HadithSchema])
async def get_all_hadith(
                        service:Hadithservice=Depends(get_hadith_service)):
    result = await service.get_all_hadith_by_query({})
    return paginate(result)

@hadis_router.delete("/{id}",response_model=dict)
async def delete_hadith_by_id(id:str,
                              current_user:UserResponse=Depends(get_current_user),
                              service:Hadithservice=Depends(get_hadith_service)):
    if current_user.role != 'admin':
        raise PermissionException
    deleted_id = await service.delete_hadith_by_id(id)
    await redis_delete(f"hadis:{id}")
    return {"deleted_id":deleted_id}

@hadis_router.put("/{id}",response_model=dict)
async def update_hadith_by_id(id:str,
                              data:HadithUpdate,
                              current_user : UserResponse=Depends(get_current_user),
                              service: Hadithservice=Depends(get_hadith_service)):
    if current_user.role != 'admin':
        raise PermissionException
    result =await  service.update_hadith_by_id(id,data)
    key =f"hadis:{id}"
    await redis_delete(key=key)
    await redis_set(key=key,val=asdict(result))
    return {"result":result}



@hadis_router.get("/random/haith",response_model=dict)
async def get_hadith_of_the_day():
    today = date.today().isoformat()
    key = f"{today}_hadith"
    hadith_data = await redis_get(key)
    if hadith_data == None:
        raise HTTPException(status_code=500,detail="celery beat doesn't work")
    return {"result":hadith_data}


add_pagination(hadis_router)