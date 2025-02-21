import smtplib
import ssl
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


def send_mail(sender, sender_alias, sender_pwd, recipient_list, bcc_mail, subject, body, host="smtp.qcloudmail.com", port=465,
              is_use_ssl=True):
    ret = False
    try:
        message = MIMEMultipart('alternative')
        message['Subject'] = Header(subject, 'UTF-8')
        message['From'] = formataddr([sender_alias, sender])
        message['To'] = ",".join(recipient_list)
        to_addr_list = recipient_list
        message['Bcc'] = ','.join(bcc_mail)

        mime_text = MIMEText(body, _subtype='html', _charset='UTF-8')
        message.attach(mime_text)

        if is_use_ssl:
            context = ssl.create_default_context()
            context.set_ciphers('DEFAULT')
            # context.options |= ssl.OP_NO_TLSv1_3  # 如果当前选择到了TLSv1_3，则使用这行来屏蔽1.3因为服务端不支持

            # 当使用了上面代码还是出现 SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure 之类的ssl错误，
            # 请先使用 pip install --upgrade ssl 来更新SSL库，重新运行，如果仍旧失败，则需要更改下面ses的支持的协议和加密算法
            # 目前ses服务端支持ssl的协议和加密套件如下：
            # ssl_protocols    TLSv1 TLSv1.1 TLSv1.2;
            # ssl_ciphers      AES128-SHA:AES256-SHA:RC4-SHA:DES-CBC3-SHA:RC4-MD5;
            # 使用下面方法来自定义协议和加密算法
            # print(f'ssl_version={ssl.OPENSSL_VERSION}')
            # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            # context.set_ciphers('AES128-SHA:AES256-SHA:RC4-SHA:DES-CBC3-SHA:RC4-MD5')

            client = smtplib.SMTP_SSL(host, port, context=context)
        else:
            client = smtplib.SMTP(host, port)

        client.login(sender, sender_pwd)
        client.sendmail(sender, to_addr_list, message.as_string())
        client.quit()
        print('Send email success!')
        ret = True
    except smtplib.SMTPConnectError as e:
        print(f'Send email failed, host: {host}, connection error:{e.smtp_code}, {e.smtp_error}')
    except smtplib.SMTPAuthenticationError as e:
        print(f'Send email failed, host: {host}, smtp authentication error:{e.smtp_code}, {e.smtp_error}')
    except smtplib.SMTPSenderRefused as e:
        print(f'Send email failed, host: {host}, sender refused:{e.smtp_code}, {e.smtp_error}')
    except smtplib.SMTPRecipientsRefused as e:
        print(f'Send email failed,host: {host}, recipients refused: {e.recipients}')
    except smtplib.SMTPDataError as e:
        print(f'Send email failed,host: {host}, smtp data error:{e.smtp_code}, {e.smtp_error}')
    except smtplib.SMTPException as e:
        print(f'Send email failed, host: {host}, smtp exception: {str(e)}')
    except Exception as e:
        print(f'Send email failed, host: {host}, other error: {str(e)}')
    return ret
