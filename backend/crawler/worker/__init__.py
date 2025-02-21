#!/usr/bin/env python
# encoding: utf-8

from crawler.worker.vuli_monitor.recycler import result_handler as vuli_monitor_result_handler
from crawler.worker.vuli_monitor.recycler import args_handler as vuli_monitor_args_handler


WORKER_MAP = {
    'task.vuli_monitor.crawler_list': {
        'task_path': 'crawler.worker.vuli_monitor.consumer.crawler_list',
        'result_handler': vuli_monitor_result_handler,
        'args_handler': vuli_monitor_args_handler
    }
}

OTHER_QUEUE_WORKER = {  # 非初始启动任务，但需要单独任务队列
    'task.vuli_monitor.crawler_detail': {
        'task_path': 'crawler.worker.vuli_monitor.consumer.crawler_detail'
    },
    'task.vuli_pusher.mail': {
        'task_path': 'crawler.worker.vuli_pusher.mail'
    },
    'task.vuli_pusher.qiyeweixin': {
        'task_path': 'crawler.worker.vuli_pusher.qiyeweixin'
    },
    'task.vuli_pusher.dingding': {
        'task_path': 'crawler.worker.vuli_pusher.dingding'
    },
    'task.vuli_pusher.feishu': {
        'task_path': 'crawler.worker.vuli_pusher.feishu'
    },
    'task.vuli_pusher.custom': {
        'task_path': 'crawler.worker.vuli_pusher.custom'
    },
}
