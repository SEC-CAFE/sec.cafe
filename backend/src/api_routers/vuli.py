import datetime
from typing import Union
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status, Body
from playhouse.shortcuts import model_to_dict

from src.models import db_object
from src.models.vul_intelligence import VulIntelligence

from src.utils.wraps import vip_required, request_limit_check
from src.routers.response import Response
from src.utils.auth import UserModel, get_api_current_user


router = APIRouter()


async def get_vuls(
        fields: list,
        limit: int = 10,
        components: list = [],
        date_range: list = [],
        title_keyword: str = ''
        ) -> Union[Response, HTTPException]:
    resp = Response()
    query = VulIntelligence.select()
    if title_keyword:
        query = query.where(VulIntelligence.title.contains(title_keyword.strip()))
    if date_range:
        query = query.where(VulIntelligence.publish_time >= date_range[0], VulIntelligence.publish_time < date_range[1])
    if components:
        query = query.where(VulIntelligence.components.contains_any(*tuple(components)))

    query = query.order_by(VulIntelligence.publish_time.desc(), VulIntelligence.id.desc()).limit(limit)
    try:
        rcds = await db_object.execute(query)
    except Exception:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取漏洞情报失败！",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        if not rcds:
            rcds = []
        data = []
        for _ in rcds:
            _ = model_to_dict(_)
            item = {}
            for _field in fields:
                item[_field] = _.get(_field)
                if _field == 'related_vuls':
                    related_vuls = []
                    for _v in item[_field]:
                        name = _v.get('source', {}).get('name')
                        _v.pop('source')
                        _v['name'] = name
                        _v['url'] = 'https://sec.cafe/url/' + _v['url']
                        related_vuls.append(_v)
                    item[_field] = related_vuls
                elif _field in ['components', 'cwes', 'tags', 'reference_links']:
                    if not _.get(_field):
                        item[_field] = []
                elif _field == 'url':
                    item[_field] = 'https://sec.cafe/url/' + _['tinyurl']
            item['publish_time'] = item['publish_time'].strftime('%Y-%m-%d')
            data.append(item)
        resp.data = data
    return resp


# @router.post("/new", response_model=Response, summary="返回最新漏洞情报")
# @request_limit_check(limit_num=30, key='api', error_msg='今天请求次数已用尽，请升级账号！')
# async def new(current_user: UserModel = Depends(get_api_current_user)):
#     """
#     return:
#     ```json
#     {
#       "id": 842,  # 漏洞ID
#       "publish_time": "2023-08-14",  # 漏洞发布时间
#       "cve": "",  # CVE编号
#       "url": "https://avd.aliyun.com/detail?id=AVD-2023-1678773",  # 漏洞详情地址
#       "title": "绿盟 SAS堡垒机 webconf/Exec/index 命令执行漏洞",  # 漏洞标题
#       "descript": "HIKVISION 视频编码设备接入网关存在任意文件下载，未经身份验证的远程攻击者可以在showFile.php接口下载任意文件", # 漏洞描述
#       "related_vuls": [ # 重复漏洞(不同来源)
#         {
#           "title": "HIKVISION 视频编码设备接入网关 任意文件下载(QVD-2023-18992)",  # 漏洞标题
#           "url": "https://nox.qianxin.com/vulnerability/detail/QVD-2023-18992",  # 漏洞详情地址
#           "name": "奇安信NOX漏洞库"  # 来源站点名
#         }
#       ],
#     }
#     ```
#     """
#     fields = ['id', 'publish_time', 'cve', 'url', 'title', 'descript', 'related_vuls']
#     return await get_vuls(fields, limit=20)


class searchIteam(BaseModel):
    keyword: str = ''
    start: str = '1'


@router.post("/new", response_model=Response, summary="返回最新漏洞情报")
# @vip_required
@request_limit_check(limit_num=30, key='api', error_msg='今天请求次数已用尽！漏洞情报更新频率为每小时，请不要过于频繁请求！')
async def new_vip(
    components: str = Body(default='',
                           title='组件名',
                           description='输入要筛选的组件名，多个组件用,分隔',
                           example="wordpress,致远OA"),
    title_keyword: str = Body(default='',
                              title='标题关键字',
                              description='输入要筛选的标题关键字',
                              example="命令执行"),
    date_range: str = Body(default='',
                           title='漏洞发布日期筛选',
                           description='筛选漏洞发布日期，格式：yyyy-mm-dd,yyyy-mm-dd, start_time<=data<end_time,格式错误默认不做时间筛选',
                           example="2023-08-01,2023-08-05"),
    current_user: UserModel = Depends(get_api_current_user)
):
    """
    参数格式请参考Schemas中的Body_new_vip_v1_vulti_new_vip_post

    return:
    ```
    {
      "id": 845, # 漏洞ID
      "related_vuls": [ # 重复漏洞(不同来源)
        {
          "title": "HIKVISION 视频编码设备接入网关 任意文件下载(QVD-2023-18992)",  # 漏洞标题
          "url": "https://nox.qianxin.com/vulnerability/detail/QVD-2023-18992",  # 漏洞详情地址
          "name": "奇安信NOX漏洞库"  # 来源站点名
        }
      ],
      "publish_time": "2023-08-16",  # 漏洞发布时间
      "cve": "", # CVE编号
      "url": "https://nox.qianxin.com/vulnerability/detail/QVD-2023-18992",  # 漏洞详情地址
      "title": "HIKVISION 视频编码设备接入网关 任意文件下载(QVD-2023-18992)",  # 漏洞标题
      "descript": "HIKVISION 视频编码设备接入网关存在任意文件下载，未经身份验证的远程攻击者可以在showFile.php接口下载任意文件", # 漏洞描述
      "cnnvd": "", # CNNVD编号
      "cnvd": "", # CNVD编号
      "components": [ # 影响组件
        "HIKVISION 视频编码设备接入网关"
      ],
      "vul_category": "信息泄露", # 风险类型
      "poc_status": "PoC", # 利用状态，null/POC/EXP
      "cwes": [], # CWE 列表
      "cvss": null, # CVSS，float or null
      "level": 3,  # 漏洞等级，1:低危，2：中危， 3：高危， 4：严重
      "patch": false,  # 是否有补丁，fasle/true
      "reference_links": [],  # 参考链接
      "update_time": "2023-08-16T13:27:26.449055",  # 更新时间
      "tags": [  # 标签
        "关键漏洞",
        "POC公开"
      ]
    },
    ```
    """
    fields = [
        'id', 'related_vuls', 'publish_time', 'cve', 'url', 'title', 'descript',
        'cnnvd', 'cnvd', 'components', 'vul_category', 'poc_status', 'cwes', 'cvss',
        'level', 'patch', 'reference_links', 'update_time', 'tags'
    ]
    if components:
        components = components.split(',')
    if date_range:
        date_range = date_range.split(',', 1)
        try:
            start_time = datetime.datetime.strptime(date_range[0], '%Y-%m-%d')
            end_time = datetime.datetime.strptime(date_range[1], '%Y-%m-%d')
            assert end_time > start_time
        except Exception:
            date_range = []
        else:
            date_range = [start_time, end_time]

    return await get_vuls(fields, limit=50, date_range=date_range, components=components, title_keyword=title_keyword)
