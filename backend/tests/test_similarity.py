#!/usr/bin/env python
# encoding: utf-8

# https://github.com/yongzhuo/Macropodus/tree/master


import pathmagic # noqa
import macropodus
from crawler.worker.vuli_monitor.vul_similarity import check_vul_similarity


def text_similarity(str1, str2):
    sents = macropodus.sim(str1, str2, type_sim="total", type_encode="avg")
    if sents > 0.7:
        print('ok')
    print(sents)
    # sents = macropodus.sim(str1, str2, type_sim="cosine", type_encode="single")
    # print(sents)


def test_similarity():
    str1 = 'SmartBI RMIServlet 远程代码执行漏洞'
    str2 = 'Smartbi 远程代码执行漏洞'
    str3 = 'Smartbi内置用户登陆绕过漏洞'
    str4 = '宏景HCM codesettree SQL注入漏洞（CNVD-2023-08743）'
    str5 = '宏景HR系统 SQL注入漏洞(CNVD-2023-08743)'
    str6 = '泛微 ofslogin.jsp 任意用户登陆漏洞'
    str7 = 'Weaver OA ofsLogin.jsp 信息泄露与前台任意用户登陆漏洞'
    str8 = '泛微OA E-Cology9 SQL注入漏洞'
    str9 = '汉得SRM tomcat.jsp 登陆绕过漏洞'
    str10 = '汉得SRM 登录绕过漏洞'

    text_similarity(str1, str2)
    text_similarity(str1, str3)
    text_similarity(str2, str3)
    text_similarity(str4, str5)
    text_similarity(str6, str7)
    text_similarity(str5, str8)
    text_similarity(str6, str8)
    text_similarity(str9, str10)


def test_similarity_vul():
    vul1 = {
        'title': 'SmartBI 特定情况下登录与权限验证漏洞',
        'descript': 'Smartbi是一款商业智能应用，提供了数据集成、分析、可视化等功能，帮助用户理解和使用他们的数据进行决策。8月22日，官方发布安全更新，修复相关漏洞，攻击者可构造恶意请求绕过登录认证。',
        'publish_time': '2023-08-28',
    }

    vul2 = {
        'title': 'SmartBI 身份认证绕过漏洞',
        'descript': 'SmartBI中存在身份认证绕过漏洞。由于QVD-2023-15129漏洞补丁可绕过，导致远程未授权攻击者仍可能通过windowUnloading参数绕过身份认证，进一步结合后台接口利用可实现远程代码执行。',
        'publish_time': '2023-08-28',
    }

    vul3 = {
        'title': 'Tencent 企业微信私有化版本 agentinfo 未授权访问漏洞',
        'descript': '企业微信是腾讯微信团队为企业打造的专业办公管理工具。2023年8月，互联网上披露其相关接口存在未授权访问漏洞，攻击者可构造恶意请求获取敏感信息，并组合调用相关API接口',
        'publish_time': '2023-08-28',
    }
    vul4 = {
        'title': '企业微信私有化版本信息泄露漏洞',
        'descript': '企业微信私有化历史版本中，在未授权情况下允许远程攻击者直接获取企业微信 secret 等敏感信息，可能导致企业微信全量数据被获取，造成敏感信息泄露。',
        'publish_time': '2023-08-28',
    }
    vul5 = {
        'title': '企业微信 /cgi-bin/gateway/agentinfo 未授权访问漏洞',
        'descript': '企业微信某接口未授权情况下可直接获取企业微信secret等敏感信息，可导致企业微信全量数据被获取，文件获取、使用企业微信轻应用对内发送钓鱼文件和链接等风险',
        'publish_time': '2023-08-28',
    }
    vul8 = {
        'title': 'kkFileView 任意文件上传致远程代码执行漏洞',
        'descript': 'kkFileView是一个开源在线文件预览解决方案。2024年4月，互联网公开披露kkFileView 任意文件上传致远程代码执行漏洞，攻击者可构造恶意请求上传恶意文件，并可能造成远程代码执行。',
        'publish_time': '2024-04-17',
        'update_time': '2024-04-17'
    }
    vul6 = {
        'title': 'kkFileView zipslip 远程代码执行漏洞',
        'descript': 'kkFileView v4.2.0~v4.4.0-beta 远程代码执行漏洞',
        'publish_time': '2024-04-16',
        'update_time': '2024-04-16'
    }
    vul7 = {
        'title': 'kkFileView 4.2.0-4.4.0 任意文件上传导致远程执行漏洞',
        'descript': 'kkFileView是使用spring boot搭建的文件文档在线预览解决方案，支持主流办公文档的在线预览。kkFileView 4.2.0 到4.4.0-beta版本中文件上传功能存在zip路径穿越问题，导致攻击者可以通过上传恶意构造的zip包，覆盖任意文件。kkFileView预览功能中会调用Libreoffice将odt文件转换为pdf，过程中会调用uno.py，攻击者可通过覆盖uno.py文件可执行任意python代码。',
        'publish_time': '2024-04-17',
        'update_time': '2024-04-17'
    }
    vul9 = {
        'title': 'kkFileView任意文件上传漏洞',
        'descript': 'kkFileView存在任意文件上传漏洞，该漏洞是由于kkFileView组件v4.2.0及以上版本中解压缩功能存在缺陷导致，攻击者可利用该漏洞在未授权的情况下，通过演示页面上传恶意构造的压缩包，可以实现覆盖系统文件，最终获取服务器权限。',
        'publish_time': '2024-04-14',
        'update_time': '2024-04-17'
    }

    # print(check_vul_similarity(vul1, vul2))
    # print(check_vul_similarity(vul3, vul4))
    # print(check_vul_similarity(vul4, vul5))
    # print(check_vul_similarity(vul3, vul5))
    # print(check_vul_similarity(vul6, vul7))
    # print(check_vul_similarity(vul6, vul8))
    print(check_vul_similarity(vul6, vul9))


if __name__ == '__main__':
    # test_similarity()
    test_similarity_vul()
