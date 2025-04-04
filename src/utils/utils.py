import time
import jwt
import logging
from datetime import datetime

from hijri_converter import convert

from passlib.context import CryptContext
# from ..dependencies import get_user_service
# from ..service.user import UserService
from ..constants import Token,ALLOWED_EXTENSIONS
from ..config.config import (ACCESS_TOKEN_EXPIRE_MINUTES,
                             JWT_KEY,ALGORITHM,REFRESH_TOKEN_EXPIRES_HOURS)


# from ..constants import Errors
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(user_id: str):
    expire = time.time() + ACCESS_TOKEN_EXPIRE_MINUTES*60
    payload = {"user_id": user_id, Token.expires: expire}
    token = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
    return token

async def create_refresh_token(user_id :str)->str:
    expire = time.time() + REFRESH_TOKEN_EXPIRES_HOURS*3600
    payload = {"user_id": user_id, Token.expires: expire}
    token = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        if decoded_token.get("expires", 0) >= time.time():
            # Токен действителен
            return decoded_token
        else:
            return None
    except Exception as e:
        logging.error("auth jwt error",e)
        return None



async def convert_georgia_time_to_hijri(georgia_time:int)->str:
    # Convert timestamp to a datetime object
    current_date = datetime.utcfromtimestamp(georgia_time)

    # Extract year, month, and day
    year = current_date.year
    month = current_date.month
    day = current_date.day

    # Convert Gregorian date to Hijri date
    hijri_date = convert.Gregorian(year, month, day).to_hijri()
    return str(hijri_date)

async def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
