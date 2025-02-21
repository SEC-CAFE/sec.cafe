#!/usr/bin/env python
# encoding: utf-8

import datetime
from src.models import db
from peewee import Model, CharField, DateTimeField


class TUrl(Model):
    class Meta:
        database = db
        table_name = 'urls'
        indexes = (
            (('code',), False),
        )

    code = CharField(max_length=6)
    url = CharField(max_length=300)
    create_time = DateTimeField(default=datetime.datetime.now)  # 创建时间
