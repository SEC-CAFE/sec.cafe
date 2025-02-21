from fastapi.responses import RedirectResponse
from fastapi import APIRouter, HTTPException, status
from src.utils.url import TinyURL
from src.models import db_object


router = APIRouter()


@router.get("/url/{code}", include_in_schema=False)
async def url_jump(code: str):
    url = None
    with db_object.allow_sync():
        url = await TinyURL.recovery(code)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="error",
        )
    else:
        return RedirectResponse(url=url)
