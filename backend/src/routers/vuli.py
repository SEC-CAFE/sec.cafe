from pydantic import BaseModel
from fastapi import APIRouter, Body
from playhouse.shortcuts import model_to_dict

from src.models import db_object
from src.models.vul_intelligence import VulIntelligence
from src.routers.response import Response, CustomException


router = APIRouter()


class searchIteam(BaseModel):
    keyword: str = ''
    start: str = '1'
    order: str = "publish_time"
    source_limit: int = 0


START = 1
LENGTH = 15


async def get_new_vulti(start: int = 1, length: int = 15, order: str = "publish_time", keyword: str = '', source_limit: int = 0):
    query = VulIntelligence.select()
    if keyword:
        keyword = keyword.strip()
        query = query.where((VulIntelligence.title.contains(keyword)) | (VulIntelligence.cve == keyword.upper()))
    if source_limit:
        query = query.where(VulIntelligence.multiple_source == True)
    if order == 'update_time':
        query = query.order_by(VulIntelligence.update_time.desc(), VulIntelligence.id.desc())
    else:
        query = query.order_by(VulIntelligence.publish_time.desc(), VulIntelligence.id.desc())

    query = query.paginate(start, length)
    rcds = await db_object.execute(query)
    data = []
    if rcds:
        for _ in rcds:
            _ = model_to_dict(_)
            item = {}
            fields = ['id', 'related_vuls', 'publish_time', 'cve', 'tinyurl', 'title', 'descript']
            for _field in fields:
                item[_field] = _.get(_field)
            item['publish_time'] = item['publish_time'].strftime('%Y-%m-%d')
            data.append(item)
    return data


@router.post("/new", response_model=Response, include_in_schema=False,
             summary="返回最新漏洞情报")
async def new(item: searchIteam = Body(...)):
    resp = Response()
    data = await get_new_vulti(START, LENGTH, item.order, item.keyword, item.source_limit)
    if data == 'error':
        raise CustomException(-1, 'Something is wrong!')
    else:
        resp.data = data
        return resp
