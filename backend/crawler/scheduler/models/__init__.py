#!/usr/bin/env python
# encoding: utf-8

from urllib import parse

from src.utils.db import gen_db
from src.utils.redis import Redis
from src.conf.config import get_app_settings


settings = get_app_settings()


scheduler_db_config = {
    'host': settings.postgres_host,
    'port': settings.postgres_port,
    'user': settings.postgres_user,
    'password': settings.postgres_password,
    'database': 'scheduler_task'
}
scheduler_db, scheduler_db_object = gen_db(scheduler_db_config)


CELERY_RESULT_URL = 'redis://:{}@{}:{}/1'.format(
    settings.redis_password,
    settings.redis_host,
    settings.redis_port
    )
task_redis = Redis(CELERY_RESULT_URL)


CELERY_BROKER_API = 'http://{}:{}@{}:{}/api'.format(
    parse.quote(settings.rabbitmq_default_user),
    parse.quote(settings.rabbitmq_default_pass),
    settings.rabbitmq_host,
    settings.rabbitmq_ui_port
)
