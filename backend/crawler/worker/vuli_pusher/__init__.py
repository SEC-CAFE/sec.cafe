#!/usr/bin/env python
# encoding: utf-8

import time
import asyncio
from loguru import logger
from src.utils.msg import HookPushMsg
from src.models import db_object
from src.models.settings import Setting
from src.models.vul_intelligence import VulIntelligence
from crawler.scheduler.app import celery_app
from crawler.scheduler.models import task_redis
from crawler.utils.remote_queue import get_queues_message_num


HMSG = HookPushMsg()
MSG_TYPES = {
    'qiyeweixin': HMSG.qiyeweixin,
    'dingding': HMSG.dingding,
    'feishu': HMSG.feishu,
    'custom': HMSG.custom,
    'mail': HMSG.mail,
}


@celery_app.task(name='task.vuli_pusher.create_task', ignore_result=True)
def create_task(debug: bool = False):
    # 获取漏洞列表及生成发送任务
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    task = loop.create_task(_create_task(debug))
    loop.run_until_complete(task)


async def _create_task(debug: bool = False):
    # 获取需要推送漏洞列表
    logger.info('Start pusher task.')
    queue_num = await get_queues_message_num('task.vuli_monitor.crawler_')
    if queue_num > 0 or queue_num == -1:  # 判断爬虫任务是否都执行完成或获取数量失败
        logger.info(f'Crawler is runing,  queue num is {queue_num}, quit task.')
    else:
        push_time = task_redis.get_or_set_pusher_status()
        if push_time:  # 判断是否有其他push任务在执行
            logger.info(f'Other pusher is runing, time is {push_time}.')
        else:
            task_redis.get_or_set_pusher_status(set=True)  # 设置执行状态
            time.sleep(60*5)  # 等待 5 分钟让爬虫任务收尾完成

            last_id = task_redis.get_or_set_pusher_id()
            logger.info(f'Query last id is [{last_id}]')
            with db_object.allow_sync():
                vul_list = []
                vuls = VulIntelligence.select().where(
                    VulIntelligence.id > last_id
                    ).order_by(
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
                    if _v.id > last_id:
                        last_id = _v.id
                logger.info('Get vul list length is [{}], new last id is [{}]'.format(len(vul_list), last_id))
                if vul_list:  # 新增漏洞为空则中断任务
                    # 生成推送任务
                    tasks = {}
                    for key in MSG_TYPES.keys():
                        tasks[key] = []

                    task_settings = Setting.select().where(Setting.key == 'hook_url')
                    for _t in task_settings:
                        push_type = _t.value['push_type']
                        tasks[push_type].append(_t.value)

                    logger.info(f'Get task settings, {str(tasks)}')

                    # 非邮件类型任务创建
                    for push_type in MSG_TYPES.keys():
                        if push_type == 'mail':
                            continue

                        num = 0
                        for _v in tasks[push_type]:
                            if debug:
                                await _pusher(vul_list, _v['hook_url'], _v['sign'], push_type, debug)
                            else:
                                celery_app.send_task(
                                    'task.vuli_pusher.{}'.format(push_type),
                                    args=(vul_list, _v['hook_url'], _v['sign'], debug)
                                )
                            num += 1
                        logger.info(f'Create {push_type} task, num: {num}')
                    # 邮件类型任务创建(增加合并逻辑)
                    receiver = []
                    length = len(tasks['mail'])
                    num = 0
                    for _v in tasks['mail']:
                        receiver.append(_v['hook_url'])
                        length -= 1

                        if len(receiver) == 1 or length <= 0:
                            if debug:
                                await _pusher(vul_list, _v['hook_url'], _v['sign'], 'mail', debug)
                            else:
                                celery_app.send_task(
                                    'task.vuli_pusher.mail',
                                    args=(vul_list, receiver, _v['sign'], debug)
                                )
                            receiver = []
                            num += 1
                    logger.info(f'Create mail task, num: {num}')

            # 更新ID标记
            logger.info(f'Update task status tag. last id is {last_id}')
            task_redis.get_or_set_pusher_id(last_id)
            task_redis.delete_pusher_status()  # 删除执行状态


@celery_app.task(name='task.vuli_pusher.mail', ignore_result=True)
def mail_pusher(vuls: list, hook_url: str, sign: str, debug: bool = False):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    task = loop.create_task(_pusher(vuls, hook_url, sign, 'mail', debug))
    loop.run_until_complete(task)
    return task.result()


@celery_app.task(name='task.vuli_pusher.qiyeweixin', ignore_result=True)
def qiyeweixin_pusher(vuls: list, hook_url: str, sign: str, debug: bool = False):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    task = loop.create_task(_pusher(vuls, hook_url, sign, 'qiyeweixin', debug))
    loop.run_until_complete(task)
    return task.result()


@celery_app.task(name='task.vuli_pusher.dingding', ignore_result=True)
def dingding_pusher(vuls: list, hook_url: str, sign: str, debug: bool = False):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    task = loop.create_task(_pusher(vuls, hook_url, sign, 'dingding', debug))
    loop.run_until_complete(task)
    return task.result()


@celery_app.task(name='task.vuli_pusher.feishu', ignore_result=True)
def feishu_pusher(vuls: list, hook_url: str, sign: str, debug: bool = False):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    task = loop.create_task(_pusher(vuls, hook_url, sign, 'feishu', debug))
    loop.run_until_complete(task)
    return task.result()


@celery_app.task(name='task.vuli_pusher.custom', ignore_result=True)
def custom_pusher(vuls: list, hook_url: str, sign: str, debug: bool = False):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    task = loop.create_task(_pusher(vuls, hook_url, sign, 'custom', debug))
    loop.run_until_complete(task)
    return task.result()


async def _pusher(vuls: list, hook_url: str, sign: str, msg_type: str, debug: bool = False):
    if debug:
        print(msg_type, hook_url)
        result = True
    else:
        func = MSG_TYPES[msg_type]
        result = await func(hook_url, vuls, sign)
    logger.info(f'Run {msg_type} task, hook_url is {hook_url}, result is [{result}]')
