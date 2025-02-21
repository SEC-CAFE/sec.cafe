#!/usr/bin/env python
# encoding: utf-8

import datetime
from playhouse.postgres_ext import BinaryJSONField

from src.models import db
from peewee import Model, BooleanField, CharField, FloatField, DateTimeField, TextField, IntegerField


class VulIBaseModel(Model):
    class Meta:
        database = db
        indexes = (
            (('title', 'publish_time'), False),
            (('publish_time',), False),
        )

    title = CharField(max_length=200)
    url = CharField(max_length=200)
    tinyurl = CharField(max_length=200, null=True)
    descript = TextField(null=True)
    cve = CharField(max_length=50, null=True)
    cnvd = CharField(max_length=50, null=True)
    cnnvd = CharField(max_length=50, null=True)
    tag_num = BinaryJSONField(null=True)
    components = BinaryJSONField(null=True)  # 影响组件与版本，[component]
    vul_category = CharField(max_length=50, null=True)  # 漏洞类型
    poc_status = CharField(max_length=10, null=True)  # null/POC/EXP
    pocs = TextField(null=True)
    cwes = BinaryJSONField(null=True)
    cvss = FloatField(null=True)
    custom_score = FloatField(null=True)  # 漏洞源自定义分数
    level = IntegerField(null=True)  # 1/2/3/4
    tags = BinaryJSONField(null=True)
    patch = BooleanField(default=False)
    patch_url = CharField(max_length=100, null=True)
    reference_links = BinaryJSONField(null=True)
    source = BinaryJSONField(default={})  # 情报来源信息，name 名称，homepage 地址，priority 优先级
    publish_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)


class OVulIntelligence(VulIBaseModel):
    class Meta:
        table_name = 'o_vul_intelligence'
        indexes = (
            (('url',), False),
        )


class VulIntelligence(VulIBaseModel):
    class Meta:
        table_name = 'vul_intelligence'

    related_vuls = BinaryJSONField(null=True)
    multiple_source = BooleanField(default=False)
    add_time = DateTimeField(default=datetime.datetime.now)
