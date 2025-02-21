#!/usr/bin/env python
# encoding: utf-8

from src.conf.config import get_app_settings

# https://docs.celeryproject.org/en/v4.4.7/userguide/configuration.html
# support multi broker_url, default use "round-robin"
settings = get_app_settings()

CELERY_BROKER_URL = 'amqp://{}:{}@{}:{}'.format(
    settings.rabbitmq_default_user,
    settings.rabbitmq_default_pass,
    settings.rabbitmq_host,
    settings.rabbitmq_port
)
CELERY_RESULT_URL = 'redis://:{}@{}:{}/1'.format(
    settings.redis_password,
    settings.redis_host,
    settings.redis_port
    )

broker_url = [
    CELERY_BROKER_URL
]
# result_backend = CELERY_RESULT_URL  # 去掉结果存储

# time second
result_expires = 24 * 3600
timezone = 'Asia/Shanghai'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

# worker_concurrency = 4

# task
task_track_started = True
