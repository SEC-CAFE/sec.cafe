from datetime import timedelta
from fastapi import APIRouter, Request, Depends, Body
from fastapi_sso.sso.github import GithubSSO

from src.models import db_object
from src.models.user import User
from src.routers.response import Response
from src.conf.config import get_app_settings
from src.utils.auth import get_current_user, create_access_token, build_auth_return_user


router = APIRouter()
settings = get_app_settings()

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
SECRET_KEY = settings.secret_key


github_sso = GithubSSO(
    client_id=settings.github_client_id,
    client_secret=settings.github_secret,
    redirect_uri="{}/auth/callback".format(settings.site_url),
    allow_insecure_http=settings.debug,
)


@router.post("/me", include_in_schema=False)
async def read_users_me(
    access_token: str = Body(embed=True),
    expire: str = Body(embed=True),
    current_user: User = Depends(get_current_user)
):
    user = build_auth_return_user(current_user, access_token, expire)
    return user


@router.get("/third_login", include_in_schema=False)
async def auth_init():
    """Initialize auth and redirect"""
    with github_sso:
        # github_url = await github_sso.get_login_redirect()
        github_url = await github_sso.get_login_url()
    return {'github': github_url}


@router.get("/github_callback", include_in_schema=False)
async def auth_callback(request: Request):
    """Verify login"""
    with github_sso:
        user = await github_sso.verify_and_process(request)
        with db_object.allow_sync():
            username = user.email if user.email else user.id
            db_user, created = User.get_or_create(username=username)
            if created:
                db_user.nickname = user.display_name
                db_user.email = user.email
                db_user.save()

            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token, expire = create_access_token(
                data={"sub": db_user.username},
                secret_key=SECRET_KEY,
                expires_delta=access_token_expires
            )
            db_user = build_auth_return_user(db_user, access_token, expire)
        return db_user
