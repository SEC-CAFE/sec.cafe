#!/usr/bin/env python
# encoding: utf-8

"""
@time: 2023/03/25 22:59:15
@desc: 通过API操作远程队列
"""

import aiohttp
from crawler.scheduler.models import CELERY_BROKER_API


async def get_queues_message_num(queue_name):
    url = CELERY_BROKER_API + '/queues'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=60) as resp:
            json_data = await resp.json()
    total_num = 0
    for q in json_data:
        if q.get('name', '').startswith(queue_name):
            num = q.get('messages', -1)
            total_num += num
            if num == -1:
                total_num = -1
                break
    return total_num
