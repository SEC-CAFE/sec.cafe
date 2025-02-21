import re
from pydantic import BaseModel
from src.models import db_object

from fastapi import APIRouter, Depends, Body
from src.utils.msg import HookPushMsg
from src.models.settings import Setting
from src.utils.auth import UserModel, get_current_user
from src.utils.wraps import request_limit_check


router = APIRouter()
hmsg = HookPushMsg()

MSG_FUNC_MAP = {
    'qiyeweixin': hmsg.qiyeweixin,
    'dingding': hmsg.dingding,
    'feishu': hmsg.feishu,
    'custom': hmsg.custom,
    'mail': hmsg.mail,
}


class VuliPushIteam(BaseModel):
    push_type: str = ''
    hook_url: str = ''
    sign: str = ''


def check_value(item):
    if not item.push_type or not item.hook_url:
        return {'type': 'error', 'msg': '类型和地址都不允许为空，请重试！'}

    if item.push_type not in MSG_FUNC_MAP.keys():
        return {'type': 'error', 'msg': '订阅类型不正确，请重试！'}

    if item.push_type == 'mail':
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    else:
        pattern = r'^https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$'

    if not re.match(pattern, item.hook_url):
        return {'type': 'error', 'msg': '请输入正确的订阅地址(仅限网址和邮箱地址)！'}
    return {}


@router.post("/get_vuli_push_url", include_in_schema=False)
async def get_vuli_push_url(current_user: UserModel = Depends(get_current_user)):
    key = 'hook_url'
    with db_object.allow_sync():
        setting = Setting.get_or_none(user=current_user, key=key)
        if not setting:
            return None
        return setting.value


@router.post("/set_vuli_push_url", include_in_schema=False)
async def set_vuli_push_url(item: VuliPushIteam = Body(...), current_user: UserModel = Depends(get_current_user)):
    cehck_result = check_value(item)
    if cehck_result:
        return cehck_result

    value = {'push_type': item.push_type, 'hook_url': item.hook_url, 'sign': item.sign}
    with db_object.allow_sync():
        key = 'hook_url'
        setting = Setting.get_or_none(user=current_user, key=key)
        if not setting:
            setting = Setting(user=current_user, key=key)
        setting.value = value
        setting.save()
        return {'type': '', 'msg': '漏洞情报订阅配置设置成功！'}


@router.post("/check_vuli_push_url", include_in_schema=False)
@request_limit_check(limit_num=30, key='check_vuli_push_url', raise_error=False, error_msg='测试失败，为避免恶意利用，每日仅限30次！')
async def check_vuli_push_url(item: VuliPushIteam = Body(...), current_user: UserModel = Depends(get_current_user)):
    cehck_result = check_value(item)
    if cehck_result:
        return cehck_result

    vuls = [
        {'title': '测试漏洞-QNAP QTS and QuTS Hero 未授权RCE', 'source_num': 2, 'publish_time': '2024-02-19'},
        {'title': '测试漏洞-Windows SmartScreen 安全功能绕过漏洞', 'source_num': 1, 'publish_time': '2024-02-18'},
        {'title': '测试漏洞-Oracle WebLogic Server 存在JNDI注入漏洞（CVE-2024-20931）', 'source_num': 3, 'publish_time': '2024-02-15'},
        {'title': '测试漏洞-GL.iNet 多个产品未授权 RCE', 'source_num': 1, 'publish_time': '2024-02-14'},
        {'title': '测试漏洞-Ivanti Pulse Connect Secure VPN SSRF致远程代码执行漏洞', 'source_num': 1, 'publish_time': '2024-02-17'},
        {'title': '测试漏洞-Linux-glibc-二进制-越界写入', 'source_num': 1, 'publish_time': '2024-02-16'},
    ]

    msg_func = MSG_FUNC_MAP[item.push_type]
    result = await msg_func(item.hook_url, vuls, item.sign)
    if not result:
        return {'type': 'error', 'msg': '请求失败，请确认配置的地址或安全方式是否正确！'}
    else:
        return {'type': '', 'msg': '已尝试提交测试漏洞情报内容，请检查！'}
