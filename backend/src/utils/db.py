#!/usr/bin/env python
# encoding: utf-8

from playhouse.db_url import connect
from playhouse.shortcuts import ReconnectMixin
from peewee_async import Manager
from peewee_async import PooledPostgresqlDatabase


# 异步数据库断线重连连接池类
class RetryPostgresqlDatabase(ReconnectMixin, PooledPostgresqlDatabase):
    _instance = None

    @staticmethod
    def get_db_instance(db_config):
        if not RetryPostgresqlDatabase._instance:
            RetryPostgresqlDatabase._instance = RetryPostgresqlDatabase(
                db_config.get('database'),
                host=db_config.get('host'),
                user=db_config.get('user'),
                password=db_config.get('password'),
                port=db_config.get('port'),
                max_connections=10,
                autoconnect=True,
            )
        else:
            if RetryPostgresqlDatabase._instance.database != db_config.get('database'):
                RetryPostgresqlDatabase._instance = RetryPostgresqlDatabase(
                    db_config.get('database'),
                    host=db_config.get('host'),
                    user=db_config.get('user'),
                    password=db_config.get('password'),
                    port=db_config.get('port'),
                    max_connections=10,
                    autoconnect=True,
                )

        return RetryPostgresqlDatabase._instance


def gen_db(db_config):
    """
    db_config = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': db_name
    }
    """
    db_config.update({
        'autorollback': True,
        'sql_mode': 'NO_AUTO_CREATE_USER',
    })
    new_db = RetryPostgresqlDatabase(**db_config).get_db_instance(db_config)
    db_obj = Manager(database=new_db)
    db_obj.database.allow_sync = False
    return new_db, db_obj


def gen_db_by_url(db_url):
    db = connect(db_url, sql_mode='NO_AUTO_CREATE_USER')
    # 使用peewee MySQLDatabase 实例化数据类，peewee-async 支持playhouse比较差
    db_config = {
        'host': db.connect_params['host'],
        'port': db.connect_params['port'],
        'user': db.connect_params['user'],
        'password': db.connect_params['passwd'],
        'database': db.database,
    }
    return gen_db(db_config)
