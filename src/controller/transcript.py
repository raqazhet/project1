from fastapi import APIRouter,Depends
from fastapi_pagination import Page,add_pagination,paginate
from dataclasses import asdict

from ..redis import redis_get,redis_set,redis_delete
from ..model.transcript import TranscriptCreate,UpdateTranscript
from ..schema.user import UserResponse
from ..schema.transcript import TrascriptSchema
from ..service.transcript import TranscriptService
from ..exceptions.exception import PermissionException
from ..dependencies import get_current_user,get_transcript_service

transcript_router = APIRouter(prefix="/transcript",tags=['transcript'])

@transcript_router.post("/",response_model=dict)
async def create_transcript(data:TranscriptCreate,
                            current_user:UserResponse=Depends(get_current_user),
                            service:TranscriptService=Depends(get_transcript_service)):
    if current_user.role !='amdin':
        raise PermissionException()
    id = await service.create_transcrip(data=data)
    return {"created_id":id}

@transcript_router.get('/all/{ayah_id}',response_model=Page[TrascriptSchema])
async def get_all_transcript_by_query(ayah_id:str,
                                        service:TranscriptService=Depends(get_transcript_service)):
    transcripts = await service.get_transcript_by_query({"ayah_id":ayah_id})
    return paginate(transcripts)

@transcript_router.get("/{id}",response_model=dict)
async def get_transcript_by_id(id:str,
                               service:TranscriptService=Depends(get_transcript_service)):
    result_data = await redis_get(key=id)
    if result_data:
        return {"result":result_data}
    result = await service.get_transcript_by_id(id=id)
    await redis_set(key=id,val=asdict(result))
    return {"result":result}

@transcript_router.put("/",response_model=dict)
async def update_transcript_data(id:str,data:UpdateTranscript,
                                 current_user:UserResponse=Depends(get_current_user),
                                 service:TranscriptService=Depends(get_transcript_service)):
    if current_user.role != 'admin':
        raise PermissionException
    result = await service.update_transcrip_data(id,data=data)
    await redis_delete(id)
    await redis_set(id,asdict(result))
    return {"result":result}

@transcript_router.delete("/{id}",response_model=dict)
async def delete_transcript_by_id(id:str,
                                  current_user:UserResponse=Depends(get_current_user),
                            service:TranscriptService=Depends(get_transcript_service)):
    if current_user.role != 'admin':
        raise PermissionException
    id = service.delete_transcript(id)
    await redis_delete(key=id)
    return {"success":f"successfully deleted transcipt by {id}"}


add_pagination(transcript_router)