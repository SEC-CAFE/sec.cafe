#!/usr/bin/env python
# encoding: utf-8

import pathmagic # noqa
from crawler.utils.content_utils import clean_title


if __name__ == '__main__':
    titles = [
        'Juniper JunOS SRX and EX 系列存在未授权 RCE（CVE-2023-36844、CVE-2023-36845、CVE-2023-36846）',
        'Spring Web UriComponentsBuilder URL解析不当漏洞(绕过)',
        'Apache ZooKeeper watchers 敏感信息泄漏（CVE-2024-23944）',
        'CVE-2024-27198：JetBrains TeamCity 身份验证绕过漏洞通告',
        'WebLogic T3/IIOP信息泄露漏洞（CVE-2024-21006/CVE-2024-21007）通告',
        'VMware vCenter Server多个高危漏洞（CVE-2024-37079/CVE-2024-37080/CVE-2024-37081）通告'
    ]
    data = {}
    for title in titles:
        print(clean_title(title, data))
