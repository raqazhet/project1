from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer

from ..utils import utils
from ..constants import Errors
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")




async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        if token is None:
            raise HTTPException(status_code=403, detail=Errors.invalid_token)
        payload = utils.decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=403, detail=Errors.invalid_token)
        username: str = payload.get("user_id")
        if username is None:
            raise HTTPException(status_code=401, detail=Errors.cntv_credentials)
    except Exception as e:
        raise HTTPException(status_code=401, detail=Errors.cntv_credentials+ e)
    user = await get_user_by(Users.email, username)
    return user