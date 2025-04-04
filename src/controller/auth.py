from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
# from fastapi_pagination import Page, paginate, add_pagination
from ..model.user import UserCreate
from ..service.user import UserService
from ..dependencies import get_user_service,get_exception_responses
from ..exceptions.exception import BaseAPIException,AlreadyExistsException,InvalidCredentialsException

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/sign-up", response_model=dict)
# responses=(BaseAPIException,AlreadyExistsException)
async def create_user(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    id =await service.create_user(user_data)
    return {"User_id": id}


@auth_router.post(
    "/sing-in",
    responses=get_exception_responses(InvalidCredentialsException),
    response_model=dict
)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                service :UserService=Depends(get_user_service)):
    # Get username and password from request body
    username = str.strip(form_data.username)
    password = str.strip(form_data.password)
    user_data={"email":username,"password":password}
    token_data = await service.sing_in_logic(user_data=user_data)
    return token_data