#!/usr/bin/env python
# encoding: utf-8

import pathmagic # noqa
import asyncio
from src.models import db_object
from src.models.user import User
from src.models.settings import Setting
from src.models.vul_intelligence import VulIntelligence
from crawler.worker.vuli_pusher import _pusher


if __name__ == '__main__':

    with db_object.allow_sync():
        vul_list = []
        vuls = VulIntelligence.select().order_by(
                VulIntelligence.publish_time.desc()
            ).limit(50)
        for _v in vuls:
            source_num = len(_v.related_vuls)
            title = '{}（{}）'.format(_v.title, _v.cve) if _v.cve else _v.title
            vul_list.append(
                {
                    'title': title,
                    'source_num': source_num,
                    'publish_time': str(_v.publish_time)[:10]
                }
            )
        _user = User.get_or_none(User.username == 'f00y1n9@gmail.com')
        task_setting = Setting.get_or_none(Setting.key == 'hook_url', Setting.user == _user)
        push_type = task_setting.value['push_type']
        urls = task_setting.value['hook_url']
        sign = task_setting.value['sign']

    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    task = loop.create_task(_pusher(vul_list, urls, sign, push_type))
    loop.run_until_complete(task)
    print(task.result())
