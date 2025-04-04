from fastapi import APIRouter,Depends
from fastapi_pagination import Page,add_pagination,paginate
from dataclasses import asdict

from ..redis import redis_delete,redis_get,redis_set
from ..service.translate import TransLateService
from ..model.transcript import TranslateCreate,TransLateUpdate
from ..schema.user import UserResponse
from ..schema.transcript import TranslateSchema
from ..exceptions.exception import PermissionException
from ..dependencies import get_translate_service,get_current_user

translate_router = APIRouter(prefix="/translate", tags=['translate'])

@translate_router.post("/",response_model=dict)
async def create_translate(data:TranslateCreate,
                           current_user:UserResponse=Depends(get_current_user),
                           service:TransLateService=Depends(get_translate_service)):
    if current_user.role != "admin":
        raise PermissionException
    id = await service.create_translate(data=data)
    return {"created_id":id}


@translate_router.get("/",response_model=dict)
async def get_transcript_by_id(id:str,
                               service:TransLateService=Depends(get_translate_service)):
    tr_data = await redis_get(id)
    if tr_data:
        return {"result":tr_data}
    result = await service.get_transcript_by_id(id)
    await redis_set(id,asdict(result))
    return {"result":result}

@translate_router.put("/{id}",response_model=dict)
async def update_data(id:str,
                      data:TransLateUpdate,
                      current_user:UserResponse=Depends(get_current_user),
                      service:TransLateService=Depends(get_translate_service)):
    if current_user.role !='admin':
        raise PermissionException
    result = await service.update_transcrip_data(id,data)
    await redis_delete(id)
    await redis_set(id,asdict(result))
    return {"result":result}


@translate_router.delete("/{id}",response_model=dict)
async def delete_translate_by_id(id:str,
                                 current_user:UserResponse=Depends(get_current_user),
                           service:TransLateService=Depends(get_translate_service)):
    if current_user.role != 'admin':
        raise PermissionException
    res_id = await service.delete_transcript(id=id)
    await redis_delete(id)
    return {"id":res_id}


@translate_router.get("/get/{ayah_id}request",response_model=Page[TranslateSchema])
async def get_request_translate(ayah_id:str,
                                service:TransLateService=Depends(get_translate_service)):
    result = await service.get_transcript_by_query({"ayah_id":ayah_id})
    return paginate(result)


add_pagination(translate_router)