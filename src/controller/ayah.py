from fastapi import APIRouter,Depends,HTTPException
from fastapi_pagination import Page, add_pagination,paginate
from dataclasses import asdict
from datetime import date

from ..model.ayah import AyahCreate
from ..exceptions.exception import PermissionDenided
from ..dependencies import get_ayah_service,get_current_user
from ..schema.user import UserResponse
from ..schema.ayah import AyahSchema
from ..service.ayah import AyahService
from ..redis import redis_get,redis_set,redis_delete

ayah_router = APIRouter(prefix="/ayah",tags=['ayah'])

@ayah_router.post("/",response_model=dict)
async def create_ayah(ayah_data:AyahCreate,current_user:UserResponse=Depends(get_current_user),
                      service:AyahService=Depends(get_ayah_service)):
    if current_user.role !="admin":
        raise HTTPException(status_code=403,detail="You don't have permissions")
    ayah_id = await service.create_ayah(data=ayah_data)
    return {"ayah_id":ayah_id}

@ayah_router.get("/{id}",response_model=dict)
async def get_ayah_by_id(id:str,
                        #  current_user:UserResponse=Depends(get_current_user),
                      service:AyahService=Depends(get_ayah_service)
                         ):
    key = f"ayah:{id}"
    ayah_data = await redis_get(key=key)
    if ayah_data:
        return {"result":ayah_data}
    result = await service.get_ayah_by_id(id=id)
    await redis_set(key=key,val=asdict(result))
    return {"ayah":result}

@ayah_router.get('/',response_model=Page[AyahSchema])
async def get_all_ayahs(service:AyahService=Depends(get_ayah_service)):
    result = await service.get_all_ayahs({})
    return paginate(result)


@ayah_router.delete("/{id}",response_model=dict)
async def delete_ayah_by_id(id:str,
                            current_user:UserResponse=Depends(get_current_user),
                            service:AyahService=Depends(get_ayah_service)):
    if current_user.role != "admin":
        raise PermissionDenided
    deleted_id = await service.delete_ayah_by_id(id=id)
    await redis_delete(f"ayah:{id}")
    return{"success":f"successfully deleted ayah by id {deleted_id}"}

@ayah_router.get('/ayah/day',response_model=dict)
async def get_ayah_of_the_day():
    key = f"{date.today().isoformat()}_ayah"
    ayah_data = await redis_get(key=key)
    if ayah_data ==None:
        raise HTTPException(status_code=500,detail="celery beat error ")
    return {"result":ayah_data}

#Pagination works in api's
add_pagination(ayah_router)
