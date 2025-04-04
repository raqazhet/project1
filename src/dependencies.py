# dependencies.py
from typing import Type, Callable, Any, List, Union

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError


from .utils.utils import decode_access_token
from .constants import Errors
from .repository.user import UserRepository
from .repository.ayah import AyahRepository
from .repository.transcript import TranscriptRepo
from .repository.translate import TransLateRepo
from .repository.hadith import HadithRepo
from .repository.likes import LikeRepo
from .repository.file import FileRepo
from .repository.dhikr import DhikrRepository
from .service.user import UserService
from .service.ayah import AyahService
from .service.translate import TransLateService
from .service.transcript import TranscriptService
from .service.hadith import Hadithservice
from .service.like import LikeService
from .service.file import FileService
from .service.dhikr import DhikrService
from .repository.db import get_database
from .exceptions.exception import BaseAPIException

db = get_database()

# def get_redis():
#     yield from create_redis()


async def get_user_service():
    return UserService(UserRepository(db=db))

async def get_ayah_service():
    return AyahService(AyahRepository(db=db))

async def get_transcript_service():
    return TranscriptService(TranscriptRepo(db=db))

async def get_translate_service():
    return TransLateService(TransLateRepo(db=db))

async def get_hadith_service():
    return Hadithservice(HadithRepo(db=db))

async def get_like_service():
    return LikeService(LikeRepo(db=db))

async def get_file_service():
    return FileService(FileRepo(db=db))

async def get_dhikr_service():
    return DhikrService(DhikrRepository(db=db))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/sing-in")

async def get_current_user(token: str = Depends(oauth2_scheme),
                           service: Type[UserService] = Depends(get_user_service)):
    try:
        if token is None:
            raise HTTPException(status_code=403, detail=Errors.invalid_token)
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=403, detail=Errors.invalid_token)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail=Errors.cntv_credentials)
    except JWTError:
        raise HTTPException(status_code=401, detail=Errors.cntv_credentials)
    user = await service.get_user_id(id=user_id)
    return user



def get_exception_responses(*args: Type[BaseAPIException]) -> dict:
    """Given BaseAPIException classes, return a dict of responses used on FastAPI endpoint definition, with the format:
    {statuscode: schema, statuscode: schema, ...}"""
    responses = dict()
    for cls in args:
        responses.update(cls.response_model())
    return responses