#!/usr/bin/env python
# encoding: utf-8

import uuid
import time
import asyncio
import datetime
from loguru import logger
from celery import signature
from celery_once import QueueOnce

from crawler.worker import WORKER_MAP
from crawler.scheduler.app import celery_app
from crawler.scheduler.models.task import SchedulerTask
from crawler.scheduler.models import scheduler_db_object


@celery_app.task(base=QueueOnce, once={'graceful': True}, name='task.result_handler', ignore_result=True)
def task_result_handler(result_data: dict, worker_name: str, record_id: str, status: int):
    @logger.catch
    async def _result_handler(result_data: dict, worker_name: str, record_id: str, status: int):
        # todo 判断重试，需要再加
        if not result_data:
            result_data = {}

        if status == 10:  # 任务链结束，则调用结果处理函数，否则只更新状态
            result_handler = WORKER_MAP.get(worker_name, {}).get('result_handler')
            logger.info('[Result Handler]Status is 10, run result_handler and save result...')
            if not result_handler:
                logger.error(f'[Result Handler]Get worker<{worker_name}>result handler fail.')
                result_data = {'error': 'result handler not exists', 'result': result_data}
            else:
                result_data = await result_handler(result_data)

        with scheduler_db_object.allow_sync():
            _task, _ = SchedulerTask.get_or_create(
                id=record_id,
                worker=worker_name
            )
            _task.result = result_data
            _task.status = status
            if status == 10:
                _task.finishTime = datetime.datetime.now()
            else:
                _task.updateTime = datetime.datetime.now()
            _task.save()
        logger.info(f'[Result Handler]Complete handler {worker_name}-{record_id}, new status: {status}.')

    logger.info(f'[Result Handler]Start handler {worker_name}-{record_id}...')
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    task = loop.create_task(_result_handler(result_data, worker_name, record_id, status))
    loop.run_until_complete(task)


@celery_app.task(base=QueueOnce, once={'graceful': True}, name='task.task_creator', ignore_result=True)
def task_creator():
    """
    周期任务，下发目标
    """
    @logger.catch
    async def _task_creator(worker_name: str, args: tuple):
        record_id = uuid.uuid5(uuid.NAMESPACE_DNS, str(time.time()))
        args = (str(record_id), ) + args
        result = celery_app.send_task(
            worker_name,
            args=args,
            chain=[
                signature('task.result_handler', args=(worker_name, str(record_id), 1))
            ]
        )
        with scheduler_db_object.allow_sync():
            await scheduler_db_object.create(
                SchedulerTask,
                id=record_id,
                worker=worker_name,
                args=args,
                task_id=result.id
            )
        logger.info(f'[Task Creator]Create task {worker_name}-{record_id}.')

    logger.info('[Task Creator]Start running...')
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    tasks = []

    for worker_name, _ in WORKER_MAP.items():
        args_handler = _['args_handler']
        logger.info('[Task Creator]Run args_handler and get tasks...')
        args = args_handler()
        for arg in args:
            tasks.append(asyncio.ensure_future(_task_creator(worker_name, (arg, ))))  # type: ignore
    loop.run_until_complete(asyncio.wait(tasks))


@celery_app.task(base=QueueOnce, once={'graceful': True}, name='task.clean_db', ignore_result=True)
def task_clean_db():
    """
    周期任务，清理数据库中任务数据
    """
    @logger.catch
    async def _clean_db():
        now = datetime.datetime.now()
        day_30_ago = now - datetime.timedelta(days=30)
        with scheduler_db_object.allow_sync():
            num = SchedulerTask.delete().where(SchedulerTask.createTime >= day_30_ago).execute()
        logger.info(f'[DB Clean]Clean tasks num: {num}.')

    logger.info('[DB Clean]Start running...')
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    task = loop.create_task(_clean_db())
    loop.run_until_complete(task)
    return task.result()
