from pydantic import BaseModel
from fastapi import APIRouter, Body
from playhouse.shortcuts import model_to_dict

from src.models import db_object
from src.models.links import Links
from src.routers.response import Response


router = APIRouter()


class searchIteam(BaseModel):
    keyword: str = ''
    start: int = 1
    length: int = 15
    type: str = "src"


@router.post("/query", response_model=Response, include_in_schema=False)
async def new(item: searchIteam = Body(...)):
    resp = Response()
    keyword = item.keyword

    query = Links.select()
    if not item.type:
        item.type = 'src'

    if item.type in ['src', 'vuldb']:
        query = query.where(Links.type == item.type)

    if keyword:
        keyword = keyword.strip()
        query = query.where((Links.name.contains(keyword)) | (Links.code.contains(keyword)) | (Links.short_name.contains(keyword)))

    start = int(item.start)
    length = int(item.length)

    # query = query.paginate(start, length)
    rcds = await db_object.execute(query)
    data = []
    if rcds:
        for _r in rcds:
            data.append(model_to_dict(_r))

    resp.data = data
    return resp
