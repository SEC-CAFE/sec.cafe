#!/usr/bin/env python
# encoding: utf-8

import json
import time
import hmac
import smtplib
import hashlib
import base64
import datetime
import urllib.parse
from loguru import logger
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from src.utils.req import HttpReq
from src.utils.mail import send_mail
from src.conf.config import get_app_settings

settings = get_app_settings()


class HookPushMsg(object):
    def __init__(self):
        self.req = HttpReq()
        self.title = 'SEC.CAFE 漏洞情报'

    def _day_str(self):
        return datetime.datetime.now().strftime('%Y/%m/%d %H')

    async def _request(self, url, method='get', params={}, headers={}, checker={}):
        retry_times = 0
        check_result = False

        while (retry_times < 3 and not check_result) or \
              (not checker and not check_result):
            text, resp = await self.req.request(
                url,
                method,
                params,
                headers,
                retry_limit=3
            )
            check_result = True
            if checker:
                if not text:
                    check_result = False
                else:
                    result = json.loads(text)
                    for key, value in checker.items():
                        if result.get(key) != value:
                            check_result = False
                            break

                if not check_result:
                    retry_times += 1

        return check_result

    async def qiyeweixin(self, hook_url, vuls, sign=''):
        length = len(vuls)
        vuls = vuls[:5]

        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "msgtype": "markdown",
            "markdown": {}
        }
        content = '## {}\n\n\n'.format(self.title)
        content += '{}新增<font color="info">{}</font>个漏洞(仅显示最新5个)：\n'.format(self._day_str(), length)
        for _ in vuls:
            content += '> - [{}] {}\n'.format(_['publish_time'], _['title'])
        content += '\n\n\n[最新漏洞列表及详情](https://sec.cafe/?order=update_time&ref=qiyeweixin)'
        data['markdown']['content'] = content

        return await self._request(hook_url, 'post', json.dumps(data), headers, checker={'errmsg': 'ok'})

    async def dingding(self, hook_url, vuls, secret=''):
        def gen_sign(secret):
            timestamp = str(round(time.time() * 1000))
            secret_enc = secret.encode('utf-8')
            string_to_sign = '{}\n{}'.format(timestamp, secret)
            string_to_sign_enc = string_to_sign.encode('utf-8')
            hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
            sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
            return timestamp, sign

        length = len(vuls)
        vuls = vuls[:5]

        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "msgtype": "markdown",
            "markdown": {'title': self.title}
        }
        content = '**{}**\n\n\n'.format(self.title)
        content += '{}新增**{}**个漏洞(仅显示最新5个)：\n'.format(self._day_str(), length)
        for _ in vuls:
            content += '> - [{}] {}\n'.format(_['publish_time'], _['title'])
        content += '\n\n\n\n[最新漏洞列表及详情](https://sec.cafe/?order=update_time&ref=dingding)'
        data['markdown']['text'] = content

        if secret:
            timestamp, sign = gen_sign(secret)
            hook_url = '{}&timestamp={}&sign={}'.format(hook_url, timestamp, sign)

        return await self._request(hook_url, 'post', json.dumps(data), headers, checker={'errmsg': 'ok'})

    async def feishu(self, hook_url, vuls, secret=''):
        def gen_sign(secret):
            timestamp = str(round(time.time()))
            string_to_sign = '{}\n{}'.format(timestamp, secret)
            hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
            sign = base64.b64encode(hmac_code).decode('utf-8')
            return timestamp, sign

        length = len(vuls)
        vuls = vuls[:5]

        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "msg_type": "post",
            "content": {'post': {'zh_cn': {'title': self.title, 'content': []}}}
        }
        contents = [[
            {
                "tag": "text",
                "text": "{}新增{}个漏洞情报(仅显示最新5个)：".format(self._day_str(), length),
            }
        ]]
        for _ in vuls:
            contents.append(
                [{
                    "tag": "text",
                    "text": " - [{}] {}".format(_['publish_time'], _['title']),
                }]
            )
        contents.append([{
                "tag": "text",
                "text": "",
            }])

        contents.append([{
            "tag": "a",
            "text": "最新漏洞列表及详情",
            "href": "https://sec.cafe/?order=update_time&ref=feishu"
        }])
        data['content']['post']['zh_cn']['content'] = contents

        if secret:
            timestamp, sign = gen_sign(secret)
            data['timestamp'] = timestamp
            data['sign'] = sign

        return await self._request(hook_url, 'post', json.dumps(data), headers, checker={'msg': 'success'})

    async def custom(self, hook_url, vuls, secret=''):
        length = len(vuls)
        vuls = vuls[:5]

        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "title": self.title,
            "time": self._day_str(),
            "num": length,
            "vuls": vuls,
            "detail_url": "https://sec.cafe/?order=update_time&ref=webhook"
        }

        return await self._request(hook_url, 'post', json.dumps(data), headers)

    async def mail(self, hook_url, vuls, secret=''):
        day_str = self._day_str()
        length = len(vuls)
        vuls = vuls[:5]
        mail_content = '''
            <html>
            <head>
            <meta http-equiv="content-type" content="text/html" charset="utf=-8">
            <meta name="viewport" content="width=device-width">
            <meta name="format-detection" content="address=no" />
            <meta name="format-detection" content="telephone=no" />
            <meta name="format-detection" content="email=no" />

            </head>

            <body style="margin: 0; padding: 0; -webkit-text-size-adjust: 100%;">
            <div style="background-color:rgb(255, 255, 255);font-size: 14px; color: #333; font-smooth: always; -webkit-font-smoothing: antialiased; ">
                <table style="table-layout: fixed;width: 100%;">
                <tr>
                    <td>
                    <table align="center" style="margin:0 auto;font-size:inherit;line-height:inherit;text-align:center;border-spacing:0;border-collapse:collapse;padding:0;border:0" cellpadding="0" cellspacing="0">
                        <tbody>
                        <tr>
                            <td style="font-family:'Lucida Grande',Helvetica,Arial,sans-serif;height:16px" height="16"></td>
                        </tr>
                        <tr>
                            <td style="width:685px">
                            <table style="font-family:'Lucida Grande',Helvetica,Arial,sans-serif;font-size:inherit;line-height:18px;padding:0px;border:0px">
                                <tbody>
                                <tr>
                                    <td style="width:40px"></td>
                                    <td style="text-align:center;width:600px">
                                    <h3>SEC.CAFE 漏洞情报</h3>
                                    </td>
                                    <td style="width:40px"></td>
                                </tr>
                                <tr>
                                    <td style="width:40px"></td>
                                    <td style="font-family:'Lucida Grande',Helvetica,Arial,sans-serif;line-height:18px;padding-top:44px;text-align:left;font-size:14px;color:#333">
                                    {} 新增{}个漏洞情报(默认只显示最新5个)：
                                    </td>
                                    <td style="width:40px"></td>
                                </tr>
        '''.format(day_str, length)
        n = 0
        for _ in vuls:
            n += 1
            vul_content = '''
                <tr>
                    <td style="width:40px"></td>
                    <td style="font-family:'Lucida Grande',Helvetica,Arial,sans-serif;line-height:18px;text-align:left;font-size:14px;color:#333;padding:17px 0 0 0">
                    {}. [{}] {}
                    </td>
                    <td style="width:40px"></td>
                </tr>
            '''.format(n, _['publish_time'], _['title'])
            mail_content += vul_content
        mail_content += '''
                                <tr>
                                    <td style="width:40px"></td>
                                    <td></td>
                                    <td style="width:40px"></td>
                                </tr>
                                <tr>
                                    <td style="width:40px"></td>
                                    <td style="text-align:left;font-family:'Lucida Grande',Helvetica,Arial,sans-serif;line-height:18px;font-size:12px;color:#333;padding:17px 0 13px 0">
                                    <a href="https://sec.cafe/?order=update_time&ref=mail" style="color:#08c;text-decoration:none" target="_blank">点击获取漏洞详情与更多漏洞情报</a>
                                    </td>
                                    <td style="width:40px"></td>
                                </tr>
                                </tbody>
                            </table>
                            </td>
                        </tr>

                        <tr style="height:17px" height="17">
                            <td style="font-family:'Geneva',Helvetica,Arial,sans-serif"></td>
                        </tr>
                        <tr>
                            <td colspan="3" background="https://ci3.googleusercontent.com/meips/ADKq_Nbp507bcljL40N0Cn3iWSF45qjHkC8BM9msWt5za56LQF7V32-U1GR6RFOCQ4wx-daV-rjvlry3iotIKfwJsQ6RcHbIHyGLFXFVvK7S9BErrTIgfP7gpmDkDnIOevY=s0-d-e1-ft#https://statici.icloud.com/emailimages/v4/common/footer_gradient_web.png" style="font-family:'Geneva',Helvetica,Arial,sans-serif;width:685px;font-size:11px;line-height:14px;color:#888;text-align:center;background-repeat:no-repeat;background-position:center top;padding:15px 0 12px" align="center">
                            <span style="white-space:nowrap">
                                <a href="https://sec.cafe" style="color:#08c;text-decoration:none" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://appleid.apple.com/choose-your-country/&amp;source=gmail&amp;ust=1708482388975000&amp;usg=AOvVaw1QcD97DZNIRf8fvIboQExj">
                                SEC.CAFE 安全咖啡
                                </a>
                            </span> |
                            <span style="white-space:nowrap">
                                <a href="https://sec.cafe/settings" style="color:#08c;text-decoration:none" target="_blank">订阅配置</a>
                            </span>
                            <br>

                            </td>
                        </tr>
                        <tr style="height:50px" height="50">
                            <td style="font-family:'Geneva',Helvetica,Arial,sans-serif">
                            </td>
                        </tr>
                        </tbody>
                    </table>
                    </td>
                </tr>
                </table>
            </div>
            </body>

            </html>
        '''
        if isinstance(hook_url, str):
            hook_url = [hook_url]
        # msg = MIMEText(mail_content, 'html', 'utf-8')
        from_email = settings.mail_user
        from_email_pwd = settings.mail_password
        from_alias = settings.mail_from
        subject_txt = '{} - {}'.format(self.title, day_str)
        body_content = mail_content
        is_using_ssl = True
        smtp_host = settings.mail_host
        smtp_port = settings.mail_port

        to_email_list = hook_url
        bcc_mail = settings.mail_bcc.split(',')
        return send_mail(from_email, from_alias, from_email_pwd, to_email_list, bcc_mail, subject_txt, body_content,
                         smtp_host, smtp_port, is_using_ssl)

        '''
        msg['Subject'] = Header('{} - {}'.format(self.title, day_str), 'utf-8')
        msg['From'] = formataddr((settings.mail_from, settings.mail_user))
        # msg['To'] = settings.mail_to
        msg['Bcc'] = ','.join(hook_url)

        try:
            # 连接到SMTP服务器并登录
            server = smtplib.SMTP(settings.mail_host, settings.mail_port)
            server.starttls()
            server.login(settings.mail_user, settings.mail_password)

            # 发送邮件
            server.sendmail(settings.mail_user, hook_url, msg.as_string())
            print("邮件已成功发送")
        except Exception as e:
            print("发送邮件时出现错误:", str(e))
            logger.error(e)
            return False
        else:
            # 关闭与SMTP服务器的连接
            server.quit()
            return True
        '''
