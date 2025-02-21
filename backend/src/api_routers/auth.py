from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.conf.config import get_app_settings
from src.utils.auth import Token, get_user, create_access_token


router = APIRouter()
settings = get_app_settings()

ACCESS_TOKEN_EXPIRE_MINUTES = settings.api_access_token_expire_minutes
SECRET_KEY = settings.api_secret_key


def authenticate_user(username: str, api_token: str):
    user = get_user(username)
    if not user:
        return False

    if user.api_token == api_token:
        return user
    else:
        return False


@router.post("/token", response_model=Token, summary="获取API请求Token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    获取API请求Token，API认证方式为Bearer认证方式，\n
    即在请求headers头配置认证信息：Authorization： Bearer Token\n
    每个Token 5分钟有效期\n
    请求参数：\n
    - username 登录邮箱地址
    - password API Token，登录后在首页右上角获取
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, expire = create_access_token(
        data={"sub": user.username},
        secret_key=SECRET_KEY,
        expires_delta=access_token_expires
    )
    data = {
        "access_token": access_token,
        "token_type": "bearer",
        "expire_time": expire.strftime('%Y-%m-%d %H:%M:%S')
    }
    return data
