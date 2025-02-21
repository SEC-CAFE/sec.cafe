from fastapi import APIRouter
from src.api_routers import vuli, auth


router = APIRouter()
router.include_router(vuli.router, tags=["漏洞情报"], prefix="/v1/vuli")
router.include_router(auth.router, tags=["认证"], prefix="/auth")
