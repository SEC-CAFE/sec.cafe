#!/usr/bin/env python
# encoding: utf-8

import datetime
from src.models import db
from src.models.user import User
from playhouse.postgres_ext import BinaryJSONField
from peewee import Model, CharField, DateTimeField, ForeignKeyField


class Setting(Model):
    class Meta:
        database = db
        table_name = 'settings'
        indexes = (
            (('user', 'key'), False),
        )

    user = ForeignKeyField(User, backref='settings')
    key = CharField(max_length=10)
    value = BinaryJSONField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)  # 创建时间
