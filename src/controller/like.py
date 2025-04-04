from fastapi import APIRouter,Depends
from fastapi_pagination import Page,paginate,add_pagination
from dataclasses import asdict
from ..model.likes import LikeCreate
from ..schema.user import UserResponse
from ..schema.like import LikeResponse
from ..dependencies import (get_current_user,get_like_service,
                            get_ayah_service,get_dhikr_service,
                            get_hadith_service)
from ..service.like import LikeService
from ..service.hadith import Hadithservice
from ..service.ayah import AyahService
from ..service.dhikr import DhikrService
from ..redis import redis_get,redis_set,redis_delete


like = APIRouter(prefix="/like",tags=['like'])

@like.post("/",response_model=dict)
async def create_like(data:LikeCreate,
                      current_user:UserResponse=Depends(get_current_user),
                      service:LikeService=Depends(get_like_service)):
    res_id = await service.create_like(current_user.id,data)
    return {"created_id":res_id}


@like.get("/{id}",response_model=dict)
async def get_like_by_id(id:str,
                         hadith_service:Hadithservice=Depends(get_hadith_service),
                         ayah_service:AyahService=Depends(get_ayah_service),
                         dhikr_service:DhikrService=Depends(get_dhikr_service),
                         service:LikeService=Depends(get_like_service)):
    key =f"like:{id}"
    like_data =await redis_get(key=key)
    if like_data:
        return {"result":like_data}
    result = await service.get_like_by_id(id=id)
    if result.card_type=="hadith":
        data = await hadith_service.get_hadith_by_id(id=result.card_id)
        lk_data = asdict(data)
        lk_data['id']=result.id
        lk_data['card_id']=result.card_id
        lk_data['card_type']=result.card_type
        lk_data['client_id']=result.client_id
        await redis_set(key=key,val=lk_data)
        return {"result":lk_data}
    elif result.card_type =="ayah":
        data = await ayah_service.get_ayah_by_id(id=result.card_id)
        lk_data = asdict(data)
        lk_data['id']=result.id
        lk_data['card_id']=result.card_id
        lk_data['card_type']=result.card_type
        lk_data['client_id']=result.client_id
        await redis_set(key=key,val=lk_data)
        return {"result":lk_data}
    else:
        data = await dhikr_service.get_dhikr_by_id(id=result.card_id)
        lk_data =data
        lk_data['id']=result.id
        lk_data['card_id']=result.card_id
        lk_data['card_type']=result.card_type
        lk_data['client_id']=result.client_id
        await redis_set(key=key,val=lk_data)
        return {"result":lk_data}


@like.get("/",response_model=Page[LikeResponse])
async def get_all_likes(current_user:UserResponse=Depends(get_current_user),
                        service:LikeService=Depends(get_like_service)):
    query ={
        "client_id":current_user.id
    }
    result = await service.get_all_likes_by_query(query=query)
    return paginate(result)


add_pagination(like)