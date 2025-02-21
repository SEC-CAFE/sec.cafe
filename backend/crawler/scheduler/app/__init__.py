#!/usr/bin/env python
# encoding: utf-8

import logging
from celery import Celery
from datetime import timedelta
from kombu import Queue, Exchange

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


from crawler.scheduler.models.db_init import init as db_init
from crawler.scheduler.app import celeryconfig
from crawler.worker import WORKER_MAP, OTHER_QUEUE_WORKER


db_init()
celery_app = Celery('sec_cafe_crawler')

# 配置sentry
if not celeryconfig.settings.debug and celeryconfig.settings.sentry_crawler_dns:
    sentry_sdk.init(
        dsn=celeryconfig.settings.sentry_crawler_dns,
        integrations=[
            CeleryIntegration(),
            LoggingIntegration(event_level=logging.ERROR)
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
    )

celery_app.config_from_object(celeryconfig)
celery_app.conf.ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': celeryconfig.CELERY_RESULT_URL,
        'default_timeout': 60 * 10
    }
}

# 周期任务配置
celerybeat_schedule_tasks = {
    'task-every-1h': {
        'task': 'task.task_creator',
        'schedule': timedelta(seconds=60*60),
        'args': ()
    },
    'task-pusher-every-10m': {
        'task': 'task.vuli_pusher.create_task',
        'schedule': timedelta(seconds=10*60),
        'args': ()
    },
    'clear-db-every-1day': {
        'task': 'task.clean_db',
        'schedule': timedelta(seconds=60*60*24),
        'args': ()
    },
}

# 初始化队列和路由
celery_queues = (Queue('task.result_handler', exchange=Exchange('task.result_handler', type='direct'), routing_key='task.result_handler'),)
router_map = {'task.result_handler': {'queue': 'task.result_handler', 'routing_key': 'task.result_handler'}}
imports = (
    'crawler.scheduler.handlers',
    'crawler.worker.vuli_pusher'
)

# 遍历worker，进行方法import和添加对应队列与路由
all_queue_workes = dict(WORKER_MAP, **OTHER_QUEUE_WORKER)
for worker_name, _ in all_queue_workes.items():
    task_name = worker_name
    func_path = _['task_path']
    imports += (func_path.rsplit('.', 1)[0],)  # type: ignore

    queue_name = task_name
    _queue = Queue(queue_name, exchange=Exchange(queue_name, type='direct'), routing_key=queue_name)
    celery_queues += (_queue,)

    router_map[task_name] = {'queue': queue_name, 'routing_key': queue_name}


# 遍历周期任务，添加对应对应队列和路由
schedule_task_names = [_['task'] for _ in celerybeat_schedule_tasks.values()]
schedule_task_names = list(set(schedule_task_names))

for name in schedule_task_names:
    _queue = Queue(name, exchange=Exchange(name, type='direct'), routing_key=name)
    celery_queues += (_queue,)
    router_map[name] = {'queue': name, 'routing_key': name}

celery_app.conf.update(
    CELERY_DEFAULT_QUEUE="sec_cafe_crawler",
    CELERY_QUEUES=celery_queues,
    CELERY_ROUTES=router_map,
    CELERY_IMPORTS=tuple(set(list(imports))),
    CELERYBEAT_SCHEDULE=celerybeat_schedule_tasks
)
