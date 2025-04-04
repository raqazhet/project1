from .exception import BadRequest,AllReadyExists
from ..constants import Messages


class UserNotFound(BadRequest):
    DETAIL ="User not found by id"


class UserAlreadyExist(AllReadyExists):
    DETAIL = "User allredy exists"
