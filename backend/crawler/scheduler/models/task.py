#!/usr/bin/env python
# encoding: utf-8


import datetime
from crawler.scheduler.models import scheduler_db
from playhouse.postgres_ext import JSONField
from peewee import Model, UUIDField, IntegerField, CharField, DateTimeField


class SchedulerTask(Model):
    class Meta:
        database = scheduler_db
        table_name = 'tasks'

        indexes = (
            (('status', 'worker'), False),
            (('task_id',), False),
        )

    id = UUIDField(primary_key=True, null=False)
    worker = CharField(max_length=50)
    args = JSONField(null=True)  # 任务参数
    task_id = CharField(max_length=100, null=True)
    status = IntegerField(default=0)  # 0 未下发 1-9 进行中 10 已完成, -1 重试
    retry_times = IntegerField(default=0)  # 重试次数
    result = JSONField(null=True)
    createTime = DateTimeField(default=datetime.datetime.now)
    updateTime = DateTimeField(default=datetime.datetime.now)
    finishTime = DateTimeField(default=datetime.datetime.now)
