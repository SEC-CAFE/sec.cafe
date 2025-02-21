#!/usr/bin/env python
# encoding: utf-8

import pathmagic # noqa
import os
import uuid
import yaml
from crawler.worker.vuli_monitor.consumer import crawler_list


def args_handler(file_name):
    # 参数处理函数，获取所有模板作为任务参数
    current_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    template_path = os.path.join(current_file_path, 'crawler/worker/vuli_monitor/templates/' + file_name)
    with open(template_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data


def check_template(template_name):
    template = args_handler(template_name)
    crawler_list(str(uuid.uuid4()), template, True)


if __name__ == '__main__':
    check_template('www.cisa.gov.yml')
