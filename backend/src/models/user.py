#!/usr/bin/env python
# encoding: utf-8

import uuid
import datetime
from playhouse.postgres_ext import JSONField

from src.models import db
from peewee import Model, CharField, DateTimeField, IntegerField, BooleanField


def new_token():
    password = str(uuid.uuid4())
    return password


class User(Model):
    class Meta:
        database = db
        table_name = 'users'
        indexes = (
            (('username',), False),
        )

    username = CharField(max_length=50)
    password = CharField(max_length=50, default=new_token)
    nickname = CharField(max_length=50, null=True)
    email = CharField(max_length=50, null=True)
    api_token = CharField(max_length=50, default=new_token)
    api_used = BooleanField(default=False)

    lab = JSONField(null=True)  # 实验功能开关

    vip_type = IntegerField(default=0)  # VIP类型，0: 未开通，1: 开通
    vip_expire_time = DateTimeField(null=True)  # VIP过期时间，endtime

    create_time = DateTimeField(default=datetime.datetime.now)  # 创建时间
    update_time = DateTimeField(default=datetime.datetime.now)  # 更新时间
