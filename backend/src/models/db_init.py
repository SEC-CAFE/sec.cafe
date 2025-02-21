#!/usr/bin/env python
# encoding: utf-8

from src.models.user import User
from src.models.url import TUrl
from src.models.links import Links
from src.models.settings import Setting
from src.models.vul_intelligence import OVulIntelligence, VulIntelligence
from src.models import db, db_object


def init():
    models = [
        OVulIntelligence, VulIntelligence,
        User, TUrl, Setting, Links
    ]
    try:
        with db_object.allow_sync():
            db.create_tables(models, safe=True)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    init()
