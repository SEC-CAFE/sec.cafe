#!/usr/bin/env python
# encoding: utf-8

import datetime
import functools
from fastapi import HTTPException, status
from src.models import api_redis


API_REQUEST_LIMIT = 30


def vip_required(func):
    @functools.wraps(func)
    async def check_vip(*arg, **kwargs):
        user = kwargs.get('current_user')
        now = datetime.datetime.now()
        if user and user.vip_type == 1 and user.vip_expire_time > now:
            pass
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足，请升级账号！",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await func(*arg, **kwargs)
    return check_vip


def request_limit_check(limit_num=API_REQUEST_LIMIT, key='api', raise_error=True, error_msg='超过请求上限！'):
    def limit_check(func):
        @functools.wraps(func)
        async def checker(*arg, **kwargs):
            user = kwargs.get('current_user')
            request_num = api_redis.get_request_times(user.username)
            if request_num < limit_num:
                try:
                    result = await func(*arg, **kwargs)
                except Exception as e:
                    raise e
                else:
                    api_redis.set_request_times(user.username)
                    return result
            else:
                if raise_error:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=error_msg,
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                else:
                    return {'type': 'error', 'msg': error_msg}
        return checker
    return limit_check
