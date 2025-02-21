from fastapi import APIRouter
from src.routers import vuli, auth, links, url, rss, settings


router = APIRouter()
router.include_router(vuli.router, tags=["Vul Intelligence"], prefix="/api/vuli")
router.include_router(auth.router, tags=["authentication"], prefix="/api/auth")
router.include_router(links.router, tags=["Links"], prefix="/api/links")
router.include_router(settings.router, tags=["settings"], prefix="/api/settings")
router.include_router(rss.router, tags=["rss"], prefix="/feed")
router.include_router(url.router, tags=["url"], prefix="")
