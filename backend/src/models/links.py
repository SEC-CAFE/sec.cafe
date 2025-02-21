#!/usr/bin/env python
# encoding: utf-8

import datetime
from src.models import db
from peewee import Model, CharField, DateTimeField, BooleanField, TextField


TYPE_CHOICES = (
    ('src', 'SRC'),
    ('vuldb', 'Vuldb'),
    ('blog', 'Blog'),
    ('social', 'Social Media'),
    ('project', 'Project'),
)


class Links(Model):
    class Meta:
        database = db
        table_name = 'links'
        indexes = (
            (('code',), False),
            (('name',), False),
            (('type', ), False),
            (('online', ), False),
        )

    code = CharField(max_length=50)
    type = CharField(choices=TYPE_CHOICES, default='src')
    name = CharField(max_length=100)
    short_name = CharField(max_length=100)
    url = CharField(max_length=200, null=True)
    tinyurl = CharField(max_length=200, null=True)
    logo = CharField(max_length=200, null=True)
    qrcode = CharField(max_length=200, null=True)
    email = CharField(max_length=50, null=True)
    wechat = CharField(max_length=50, null=True)
    twitter = CharField(max_length=50, null=True)
    weibo = CharField(max_length=50, null=True)
    descript = TextField(null=True)
    online = BooleanField(default=True)

    create_time = DateTimeField(default=datetime.datetime.now)  # 创建时间
    update_time = DateTimeField(default=datetime.datetime.now)  # 更新时间
