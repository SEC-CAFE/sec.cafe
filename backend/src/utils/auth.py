import time
from typing import Union
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from playhouse.shortcuts import model_to_dict
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.models import db_object
from src.models.user import User
from src.models import api_redis
from src.conf.config import get_app_settings


class Token(BaseModel):
    access_token: str
    token_type: str
    expire_time: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserModel(BaseModel):
    username: str
    nickname: Union[str, None] = None


settings = get_app_settings()
ALGORITHM = "HS256"
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 15
SECRET_KEY = settings.secret_key
API_SECRET_KEY = settings.api_secret_key

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")
api_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def build_auth_return_user(user, access_token, expire):
    user = model_to_dict(user)
    user.pop('password')
    user['access_token'] = access_token
    user['access_token_expire_time'] = expire.strftime('%Y-%m-%d %H:%M:%S') if not isinstance(expire, str) else expire
    user['vip_expire_time'] = user['vip_expire_time'].strftime('%Y-%m-%d %H:%M:%S') if user.get('vip_expire_time') else ''
    return user


def get_user(username: str):
    with db_object.allow_sync():
        user = User.get_or_none(username=username)
        return user


def create_access_token(data: dict, secret_key: str, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if not expires_delta:
        expires_delta = timedelta(minutes=DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.today() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)

    double_time = timedelta.total_seconds(expires_delta) * 2 + time.time()
    api_redis.set_access_token(encoded_jwt, double_time, data['sub'])
    return encoded_jwt, expire


def decode_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        return None


async def _get_current_user(token, secret_key):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_token(token, secret_key)
    if not token_data:
        raise credentials_exception

    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return await _get_current_user(token, SECRET_KEY)


async def get_api_current_user(token: str = Depends(api_oauth2_scheme)):
    user = await _get_current_user(token, API_SECRET_KEY)
    if not user.api_used:
        with db_object.allow_sync():
            user.api_used = True
            user.save()
    return user
