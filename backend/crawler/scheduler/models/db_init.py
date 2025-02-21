#!/usr/bin/env python
# encoding: utf-8

from crawler.scheduler.models.task import SchedulerTask
from crawler.scheduler.models import scheduler_db, scheduler_db_object


def init():
    models = [
        SchedulerTask,
    ]
    try:
        with scheduler_db_object.allow_sync():
            scheduler_db.create_tables(models, safe=True)
    except Exception:
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    init()
